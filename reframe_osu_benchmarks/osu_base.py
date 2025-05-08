# reframe_osu_benchmarks/osu_base.py
import reframe as rfm
import reframe.utility.sanity as sn
import os

PLACEMENT_CONFIG = {
    'on_same_numa_node': {
        'num_nodes': 1, 'num_tasks_per_node': 2,
        'launcher_options': ['--map-by numa:PE=1', '--bind-to core'],
        'descr': 'Processes on the same NUMA node'
    },
    'on_same_socket_diff_numa_nodes': {
        'num_nodes': 1, 'num_tasks_per_node': 2,
        'launcher_options': ['--map-by socket', '--bind-to numa'],
        'descr': 'Processes on same socket, different NUMA nodes'
    },
    'on_same_node_diff_sockets': {
        'num_nodes': 1, 'num_tasks_per_node': 2,
        'slurm_options': ['--ntasks-per-socket=1'],
        'launcher_options': ['--map-by socket', '--bind-to core'],
        'descr': 'Processes on different sockets, same node'
    },
    'on_diff_nodes': {
        'num_nodes': 2, 'num_tasks_per_node': 1,
        'launcher_options': ['--map-by node', '--bind-to core'],
        'descr': 'Processes on different nodes'
    }
}

class OSUBenchmarkBase(rfm.RegressionTest):
    osu_version = '7.2'
    base_modules_list = ['env/testing/2023b', 'system/hwloc']

    # Standard ReFrame parameterization: class attribute is an iterable
    placement = list(PLACEMENT_CONFIG.keys())

    executable_name = None
    message_size_param = None
    target_message_size = None
    perf_pattern = None
    perf_unit = None
    reference_value_aion = None
    reference_value_iris = None

    def __init__(self, **kwargs): # Keep **kwargs for robustness
        super().__init__(**kwargs)

        current_placement_key_for_instance = self.placement

        # --- Start of Debugging Check ---
        if not isinstance(current_placement_key_for_instance, str):
            error_msg = (
                f"OSUBenchmarkBase.__init__: self.placement is of type {type(current_placement_key_for_instance)} "
                f"with value '{current_placement_key_for_instance}', not a string as expected for a "
                f"parameterized test instance. This is the core issue."
            )
            print(f"CRITICAL WARNING: {error_msg}")
        # --- End of Debugging Check ---

        placement_cfg_data = PLACEMENT_CONFIG[current_placement_key_for_instance]

        self.valid_systems = ['aion:cpu', 'iris:cpu']
        self.valid_prog_environs = ['foss_2023b_openmpi']
        self.num_tasks = 2
        self.num_cpus_per_task = 1
        self.num_nodes = placement_cfg_data['num_nodes']
        self.job.num_tasks_per_node = placement_cfg_data.get('num_tasks_per_node')
        self.job.launcher.options = placement_cfg_data.get('launcher_options', [])
        if hasattr(self.job, 'scheduler') and self.job.scheduler and self.job.scheduler.registered_name == 'slurm':
            self.job.sched_access_opts = placement_cfg_data.get('slurm_options', [])
        self.executable_opts = ['-x', '100', '-i', '200']
        self.modules = list(self.base_modules_list)
        self.tags = {'osu', 'mpi', current_placement_key_for_instance}

    @run_before('sanity')
    def set_sanity_and_performance_patterns(self):
        if not self.executable_name:
            sn.assert_false(True, msg="executable_name not set in test class before sanity hook.")
            return

        if self.target_message_size and self.perf_pattern and self.perf_unit:
            self.sanity_patterns = sn.assert_found(
                rf'^{self.target_message_size}\s+\S+', self.stdout
            )
            extracted_value = sn.extractsingle(self.perf_pattern, self.stdout, 1, float)
            current_sys_name = self.current_system.name
            ref_val = None
            if current_sys_name == 'aion': ref_val = self.reference_value_aion
            elif current_sys_name == 'iris': ref_val = self.reference_value_iris
            perf_var_name = f'{self.executable_name}_{self.placement}_{self.perf_unit}' # self.placement here should be the string
            self.perf_patterns = {perf_var_name: extracted_value}
            if ref_val is not None:
                low_tolerance = 0.80
                high_tolerance_latency = 1.5
                if self.perf_unit == 'us':
                    reference_range = (ref_val * low_tolerance, ref_val * high_tolerance_latency)
                elif self.perf_unit == 'MB/s':
                    reference_range = (ref_val * low_tolerance, None)
                else:
                    reference_range = (None, None)
                self.reference = {f'*:{self.current_partition.name}': {perf_var_name: reference_range}}
            else:
                self.reference = {f'*:{self.current_partition.name}': {perf_var_name: (None,)}}
        else:
            self.sanity_patterns = sn.assert_true(False, msg="Test not configured for perf.")

    @run_before('run')
    def set_executable_options(self):
        if not self.executable_name: return
        current_exe_opts = list(self.executable_opts)
        if self.message_size_param: current_exe_opts.append(self.message_size_param)
        self.executable_opts = current_exe_opts


class OSUFromSource(OSUBenchmarkBase):
    build_system = 'Autotools'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sourcesdir = None
        self.sourcepath = f'osu-micro-benchmarks-{self.osu_version}.tar.gz'
        self.build_system.cc = 'mpicc'
        self.build_system.cxx = 'mpicxx'
        self.build_system.ftn = 'mpifort'
        self.build_system.max_concurrency = 8
        self.build_system.srcdir = f'osu-micro-benchmarks-{self.osu_version}'
        self.tags.add('source_compiled')
        if self.executable_name: self.tags.add(self.executable_name)

    @run_before('compile')
    def download_osu_if_needed(self):
        self.prebuild_cmds = [f'wget -nc https://mvapich.cse.ohio-state.edu/download/mvapich/{self.sourcepath}']
        if self.executable_name:
            self.executable = os.path.join(self.build_system.srcdir, 'mpi', 'pt2pt', self.executable_name)
        else:
            print(f"WARNING in OSUFromSource.download_osu_if_needed: self.executable_name is not set for {type(self).__name__} / {self.name}")


class OSUFromEasyBuildCompileOnly(rfm.CompileOnlyRegressionTest):
    osu_version = '7.2'
    base_eb_compile_modules = ['env/testing/2023b']
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.valid_systems = ['aion:cpu', 'iris:cpu']
        self.valid_prog_environs = ['foss_2023b_openmpi']
        self.modules = list(self.base_eb_compile_modules)
        self.build_system = 'EasyBuild'
        self.build_system.easyconfig = f'osu_micro_benchmarks-{self.osu_version}-foss-2023b.eb'
        self.build_system.options = ['--robot-paths=./easyconfigs']
        self.build_system.max_concurrency = 8
        self.tags = {'osu', 'mpi', 'easybuild_compiled', 'compilation_test'}
        self.sanity_patterns = sn.assert_not_found(r'(?i)(\sERROR|Traceback)', self.stderr)


class OSUAssumePrebuiltModule(OSUBenchmarkBase):
    def __init__(self, module_to_load_list, **kwargs):
        super().__init__(**kwargs)
        self.modules.extend(module_to_load_list)

    @run_before('run')
    def _set_executable_for_prebuilt(self):
        super().set_executable_options()
        if self.executable_name and not self.executable:
            self.executable = self.executable_name
        elif not self.executable_name:
             print(f"WARNING in OSUAssumePrebuiltModule._set_executable_for_prebuilt: self.executable_name is not set for {type(self).__name__} / {self.name}")


class OSUFromEESSI(OSUAssumePrebuiltModule):
    def __init__(self, **kwargs):
        eessi_osu_module = f'OSU/{self.osu_version}-gompi-2023b'
        super().__init__(module_to_load_list=[eessi_osu_module], **kwargs)
        self.valid_prog_environs = ['eessi']
        self.tags.add('eessi_loaded')
        if self.executable_name: self.tags.add(self.executable_name)
