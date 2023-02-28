#!/usr/bin/env bash
#SBATCH --time=24:00:00
#SBATCH --job-name=co2_pw2wan
#SBATCH --output=./out/slurm_pw2wan.out
#SBATCH --partition=ccq
#SBATCH --constraint=skylake
#SBATCH --mail-type=all
#SBATCH --mail-user=landerson@flatironinstitute.org

source ~/qe_env.sh 

# source run_co2_ecut.sh
# source ./convergence_test/run_co2_kpoints.sh

# mpirun -np 30 pw.x -in bands.in > out/bands.out
# mpirun -np 30 pw.x -in pwscf.in > out/pwscf_888.out

# mpirun -np 30 pw.x -in nscf.in > out/nscf_444kpt.out
mpirun -np 30 pw2wannier90.x -in pw2wan.in > ./out/pw2wan.out

