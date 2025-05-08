# Project: ReFrame OSU Micro-Benchmark Regression Tests

## Objective
The objective of this project is the creation of ReFrame regression tests that measure intranode and internode MPI latency and bandwidth on ULHPC clusters (Aion, Iris). The tests use OSU Micro-Benchmarks (v7.2) and cover different methods of sourcing the benchmark binaries: compiled from source, compiled with EasyBuild, and loaded from the EESSI distribution.

## Prerequisites

### Software
*   **Git**: For cloning this repository.
*   **Conda (Recommended)**: For managing the Python environment and ReFrame installation.
*   **Python**: Python 3.8 or newer.
*   **ReFrame Framework**: The regression testing framework. Installation via Conda is recommended (see Setup).

### Resources
*   **OSU Micro-Benchmarks Source**: The tarball `osu-micro-benchmarks-7.2.tar.gz` is required for tests that compile from source. The tests will attempt to download it using `wget` if not present in the working directory.
*   **Access to ULHPC Clusters**:
    *   Aion and Iris clusters.
    *   Required Lmod modules:
        *   `env/testing/2023b` (providing `foss/2023b` toolchain and OpenMPI).
        *   `system/hwloc` (for system architecture information).
        *   The specific EESSI module providing OSU Micro-Benchmarks 7.2 (e.g., `OSU/7.2-gompi-2023b` - verify exact name).
        *   If using pre-installed EasyBuild OSU modules: the name of that module (e.g., `OSU-Micro-Benchmarks/7.2-foss-2023b`).
*   **EasyConfig File**:
    *   An EasyConfig file (`easyconfigs/osu_micro_benchmarks-7.2-foss-2023b.eb`) is provided for the EasyBuild compilation test.
    *   **Important**: You must update the `checksums` field in this EasyConfig file with the correct SHA256 checksum for `osu-micro-benchmarks-7.2.tar.gz`.

## Repository Structure

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory>


# GroupProject
