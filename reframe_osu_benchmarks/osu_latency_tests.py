# reframe_osu_benchmarks/osu_latency_tests.py (Attempt 2 with this structure)

import reframe as rfm
import reframe.utility.sanity as sn
import os

# --- Copied from osu_base.py for this focused debugging step ---
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
    placement = list(PLACEMENT_CONFIG.keys()) # Parameter defined here
    executable_name = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        current_placement_key_for_instance = self.placement
        if not isinstance(current_placement_key_for_instance, str):
            error_msg = (
                f"OSUBenchmarkBase.__init__: self.placement is of type {type(current_placement_key_for_instance)} "
                f"with value '{current_placement_key_for_instance}', not a string."
            )
            print(f"CRITICAL WARNING: {error_msg}")
            # For this test, if it's not a string, subsequent code will fail.
            # If this warning appears, the test discovery/parameterization isn't working as expected.
        
        # This line will fail if current_placement_key_for_instance is still a list
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
        self.tags = {'osu_base_debug', 'mpi', current_placement_key_for_instance}

    @run_before('run')
    def set_exec_for_debug(self):
        if self.executable_name:
            self.executable = self.executable_name
        else:
            print(f"WARNING: executable_name not set for {type(self).__name__} (placement: {self.placement})")
            self.executable = 'echo'
            if not hasattr(self, 'executable_opts') or not isinstance(self.executable_opts, list):
                self.executable_opts = [] # Ensure it's a list
            self.executable_opts.append(f"Error_executable_name_not_set_for_{type(self).__name__}_placement_{self.placement}")

    @run_before('sanity')
    def minimal_sanity_for_debug(self):
        if self.executable == 'echo' and any("Placement_is_" in opt for opt in self.executable_opts):
             self.sanity_patterns = sn.assert_found(r'Placement_is_', self.stdout)
        elif self.executable == 'echo' and any("Error_executable_name_not_set" in opt for opt in self.executable_opts):
            self.sanity_patterns = sn.assert_found(r'Error_executable_name_not_set', self.stdout)
        else:
            self.sanity_patterns = sn.assert_true(True)
# --- End of Copied/Simplified OSUBenchmarkBase ---


# --- Minimal Derived OSU Test ---
# REMOVE @rfm.simple_test
class DebugOSUPlacementTest(OSUBenchmarkBase): # Inherits 'placement' parameter
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.executable_name = "echo"

        # executable_opts is initialized in base, just append
        self.executable_opts.append(f"Placement_is_{self.placement}") # self.placement SHOULD be a string here

        self.tags.add('debug_osu')
        if self.executable_name:
            self.tags.add(self.executable_name)


# --- Keep MyMinimalTest as a control ---
@rfm.simple_test
class MyMinimalTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.valid_systems = ['aion:cpu', 'iris:cpu']
        self.valid_prog_environs = ['foss_2023b_openmpi']
        self.executable = 'echo'
        self.executable_opts = ['Hello from ReFrame on Aion Minimal']
        self.sanity_patterns = sn.assert_found(r'Hello from ReFrame', self.stdout)
        self.tags = {'minimal', 'debug'}
