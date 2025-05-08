#!/bin/bash
#SBATCH --job-name="rfm_MyMinimalTest"
#SBATCH --ntasks=1
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
module load env/testing/2023b
module load toolchain/foss/2023b
module load env/testing/2023b
mpirun -np 1 echo Hello from ReFrame on Aion Minimal
