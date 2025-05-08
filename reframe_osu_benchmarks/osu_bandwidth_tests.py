import reframe as rfm
from osu_base import (OSUFromSource, OSUAssumePrebuiltModule, OSUFromEESSI)
# PLACEMENT_CONFIG is defined and used within OSUBenchmarkBase now

# --- OSU Bandwidth Test (Compiled from Source) ---
# No @rfm.parameterized_test decorator
class OSUBandwidthSource(OSUFromSource):
    # No placement_key, add **kwargs
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # No placement_key
        self.executable_name = 'osu_bw'
        self.target_message_size = 1048576 # 1MB
        self.perf_pattern = rf'^{self.target_message_size}\s+(\d+\.\d+)'
        self.perf_unit = 'MB/s'
        self.tags.add('bandwidth')
        if self.executable_name: self.tags.add(self.executable_name)

        # self.placement is inherited from OSUBenchmarkBase and should be a string here
        aion_bw_refs = {
            'on_same_numa_node': 18000, 'on_same_socket_diff_numa_nodes': 17000,
            'on_same_node_diff_sockets': 15000, 'on_diff_nodes': 12000
        }
        iris_bw_refs = {
            'on_same_numa_node': 17500, 'on_same_socket_diff_numa_nodes': 16500,
            'on_same_node_diff_sockets': 14500, 'on_diff_nodes': 11000
        }
        self.reference_value_aion = aion_bw_refs.get(self.placement)
        self.reference_value_iris = iris_bw_refs.get(self.placement)

# No @rfm.parameterized_test decorator
class OSUBandwidthEasyBuildLoaded(OSUAssumePrebuiltModule):
    # No placement_key, add **kwargs
    def __init__(self, **kwargs):
        eb_module_name = f'OSU-Micro-Benchmarks/{self.osu_version}-foss-2023b'
        super().__init__(module_to_load_list=[eb_module_name], **kwargs) # No placement_key
        self.executable_name = 'osu_bw'
        self.target_message_size = 1048576
        self.perf_pattern = rf'^{self.target_message_size}\s+(\d+\.\d+)'
        self.perf_unit = 'MB/s'
        self.tags.add('bandwidth')
        self.tags.add('easybuild_loaded')
        if self.executable_name: self.tags.add(self.executable_name)

        aion_bw_refs_eb = {
            'on_same_numa_node': 18000, 'on_same_socket_diff_numa_nodes': 17000,
            'on_same_node_diff_sockets': 15000, 'on_diff_nodes': 12000
        }
        iris_bw_refs_eb = {
            'on_same_numa_node': 17500, 'on_same_socket_diff_numa_nodes': 16500,
            'on_same_node_diff_sockets': 14500, 'on_diff_nodes': 11000
        }
        self.reference_value_aion = aion_bw_refs_eb.get(self.placement)
        self.reference_value_iris = iris_bw_refs_eb.get(self.placement)

# No @rfm.parameterized_test decorator
class OSUBandwidthEESSI(OSUFromEESSI):
    # No placement_key, add **kwargs
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # No placement_key
        self.executable_name = 'osu_bw'
        self.target_message_size = 1048576
        self.perf_pattern = rf'^{self.target_message_size}\s+(\d+\.\d+)'
        self.perf_unit = 'MB/s'
        self.tags.add('bandwidth')
        if self.executable_name: self.tags.add(self.executable_name)

        aion_bw_refs_eessi = {
            'on_same_numa_node': 18000, 'on_same_socket_diff_numa_nodes': 17000,
            'on_same_node_diff_sockets': 15000, 'on_diff_nodes': 12000
        }
        iris_bw_refs_eessi = {
            'on_same_numa_node': 17500, 'on_same_socket_diff_numa_nodes': 16500,
            'on_same_node_diff_sockets': 14500, 'on_diff_nodes': 11000
        }
        self.reference_value_aion = aion_bw_refs_eessi.get(self.placement)
        self.reference_value_iris = iris_bw_refs_eessi.get(self.placement)
