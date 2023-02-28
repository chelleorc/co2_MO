#!/usr/bin/env bash
#SBATCH --time=24:00:00
#SBATCH --job-name=co2_bands_qe
#SBATCH --output=./out/slurm_qe.out
#SBATCH --partition=ccq
#SBATCH --constraint=skylake
#SBATCH --mail-type=all
#SBATCH --mail-user=landerson@flatironinstitute.org

source ~/qe_env.sh 

# source ./convergence_test/run_co2_ecut.sh
# source run_co2_kpoints.sh

# mpirun -np 30 pw.x -in pwscf.in > out/pwscf.out
mpirun -np 30 pw.x -in bands.in > out/bands.out
# bands.x < bands_pp.in > qe_bands/bands_pp.out