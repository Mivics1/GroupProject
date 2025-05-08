# config/ulhpc_config.py

site_configuration = {
    'systems': [
        {
            'name': 'aion',
            'descr': 'Aion cluster',
            'hostnames': [r'aion-[0-9]+'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'cpu',
                    'scheduler': 'slurm',
                    'launcher': 'mpirun', # srun might be preferred if OpenMPI is SLURM-aware
                    'environs': ['foss_2023b_openmpi'],
                    'max_jobs': 8, # Adjust as needed
                    # Add hwloc module if needed globally for discovery,
                    # though tests can load it specifically
                    'modules': ['env/testing/2023b','toolchain/foss/2023b'], # Or load in tests
                }
            ]
        },
        {
            'name': 'iris',
            'descr': 'Iris cluster',
            'hostnames': [r'iris-[0-9]+'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'cpu', # Or 'batch', 'interactive' - check your cluster
                    'scheduler': 'slurm',
                    'launcher': 'mpirun',
                    'environs': ['foss_2023b_openmpi'],
                    'max_jobs': 8,
                    'modules': ['env/testing/2023b','toolchain/foss/2023b'], # Or load in tests
                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'foss_2023b_openmpi',
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort',
            'modules': ['env/testing/2023b'], # Meta-module providing foss/2023b and OpenMPI
            'target_systems': ['aion', 'iris']
        },
        {
            'name': 'eessi_osu', # Environment for EESSI binaries
            'modules': ['OSU/7.2-EESSI-foss-2023b'], # Hypothetical EESSI module for OSU
            'target_systems': ['aion', 'iris']
            # No cc, cxx, ftn needed if only using pre-compiled binaries
        }
    ],
    'logging': [
        # ... your logging config ...
    ],
    'general': [
        # ... general settings ...
        {
            'check_search_path': ['./reframe_osu_benchmarks']
        }
    ]
}
