'''
Read in kpoints.x output file to dataframes
Read out kpoints + weights to new kpoints.txt file 
    in a more readable format for nscf.in
'''

import numpy as np
import pandas as pd
from ase.dft.kpoints import *
from ase.build import bulk as crystal

# atoms = crystal('CO2','fcc',a=5.5,cubic=True)
# print(atoms.cell)
# k_mesh = get_special_points(atoms,lattice=fcc,esp=0.0002)
# k_mesh=monkhorst_pack((9,9,9))
# print(k_mesh)
## Note: Add column names to kpoints.out file for this to work
# col = ["row_num","kpoints1", "kpoints2", "kpoints3", "weight", "other"]
col = ["kpoints1", "kpoints2", "kpoints3", "weight"]
co2_kpt  = pd.read_csv('kmesh_qe.txt', names=col,delim_whitespace=True,header=1)

# co2_kpt  = pd.read_csv('/mnt/home/landerson1/projects/tight_binding/wannier90/co2_MO/co2_kpoints729.dat', names=col,delim_whitespace=True,header=1)
# change data types from objects to the datatypes (which is "guessed" by the interpreter)
co2_kpt.convert_dtypes().dtypes

# change data type for weight from float to int64
co2_kpt["weight"] = pd.Series(co2_kpt["weight"], dtype="Int64")

# convert int64 to int8 which converts to whole numbers 
# pd.to_numeric(co2_kpt["weight"], downcast='integer')
# pd.set_option('display.float_format','{:.0f}'.format)
print(co2_kpt[["kpoints1","kpoints2","kpoints3"]].to_string(index=False))
# print(co2_kpt["kpoints1"].to_string(index=False))