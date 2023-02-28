#!/bin/sh
# reminder: from now on, what follows the character # is a comment
####################################################################
#
# define the following variables according to your needs
#
outdir=./convergence_test/out
pseudo_dir=../pseudo
# the following is not actually used:
# espresso_dir=top_directory_of_espresso_package
####################################################################

# make data directory if it doesn't already exist
mkdir -p _data 

# set up input and output files
input=pwscf.in
raw_output=_data/pwscf.out
processed_output=_data/co2_ecut.csv
wfc=/mnt/home/landerson1/ceph/projects/wannier/co2/wfc

rm -f $processed_output $raw_output

for ecutwfc in 58.0 60.0 62.0 64.0 66.0 68.0; do

   echo "ecut: ${ecutwfc}" 

# self-consistent calculation
cat > $input << EOF
&CONTROL
  calculation = 'scf'
  etot_conv_thr =   1.2000000000d-04
  forc_conv_thr =   1.0000000000d-04
  outdir = './out/'
  prefix = 'CO2'
  pseudo_dir = './pseudo/'
  tprnfor = .true.
  tstress = .true.
/
&SYSTEM
  degauss =   1.4699723600d-02
  ecutrho =   4.0000000000d+02
  ecutwfc =   $ecutwfc
  ibrav = 0
  nat = 12
  nosym = .true.
  ntyp = 2
  occupations = 'smearing'
  smearing = 'cold'
  nbnd = 48
/
&ELECTRONS
  conv_thr =   2.4000000000d-09
  diagonalization = 'david'
  electron_maxstep = 80
  mixing_beta =   4.0000000000d-01
/
ATOMIC_SPECIES
C      12.0107 C.pbesol-n-rrkjus_psl.1.0.0.UPF
O      15.9994 O.pbesol-n-rrkjus_psl.1.0.0.UPF
ATOMIC_POSITIONS {crystal}
C            0.0000000000       0.0000000000       0.0000000000 
C            0.5000000000       0.0000000000       0.5000000000 
C            0.5000000000       0.5000000000       0.0000000000 
C            0.0000000000       0.5000000000       0.5000000000 
O            0.1225369800       0.1225369800       0.1225369800 
O            0.8774630200       0.8774630200       0.8774630200 
O            0.3774630200       0.8774630200       0.6225369800 
O            0.6225369800       0.1225369800       0.3774630200 
O            0.6225369800       0.3774630200       0.8774630200 
O            0.3774630200       0.6225369800       0.1225369800 
O            0.8774630200       0.6225369800       0.3774630200 
O            0.1225369800       0.3774630200       0.6225369800 
K_POINTS {automatic}
8 8 8 0 0 0
CELL_PARAMETERS angstrom
      5.4970732800       0.0000000000       0.0000000000
      0.0000000000       5.4970732800       0.0000000000
      0.0000000000       0.0000000000       5.4970732800
EOF

   # If pw.x is not found, specify the correct value for $espresso_dir,
   # use $espresso_dir/bin/pw.x instead of pw.x

   mpirun -np 30 pw.x -in $input > $raw_output

   # grep -e 'kinetic-energy cutoff' -e ! si.scf.out | \
         # awk '/kinetic-energy/{ecutwfc=$(NF-1)}/!/{print ecutwfc, $(NF-1)}' >> out/si.etot_vs_ecut_data

   # set each grep variable to get energy cutoff, total energy, and wall times for each iteration
   cutoff="$(grep -e 'kinetic-energy cutoff' ${raw_output} | awk '{print $(NF-1)}')"
   total_energy="$(grep ! ${raw_output} | awk '{print $(NF-1)}')"
   wall_time="$(grep 'PWSCF.*WALL' ${raw_output} | awk '{printf $(NF-1)}' | head -c -1)" 

   # send processed output to csv file
   echo "${cutoff}, ${total_energy}, ${wall_time}" >> $processed_output
done
