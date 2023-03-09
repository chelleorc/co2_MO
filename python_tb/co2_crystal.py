import numpy as np
import scipy
import pyscf
from pyscf.pbc import gto, dft, scf
from pyscf.tools import molden

'''
CO2 crystal
'''
# gto: Gaussian-type orbitals
cell = gto.Cell()
cell.atom = '''
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
'''
cell.pseudo = 'gth-pbe'
# (sto-ng) Slater-type orbitals where n represents the number of 
#   Gaussian primitive functions
cell.basis = 'sto6g'
cell.a = [[5.4970732800, 0.0000000000, 0.0000000000],
          [0.0000000000, 5.4970732800, 0.0000000000],
          [0.0000000000, 0.0000000000, 5.4970732800]]
# cell.verbose = 4

cell.build()

# Notes: Does not converge. Potential solutions:
##  - include smearing
kpts = cell.make_kpts([4,4,4])

#non-relativistic restricted Kohn-Sham for periodic systems for 
# periodic systems with k-point sampling
mf = dft.KRKS(cell, kpts=kpts).density_fit().run()
# print(mf)
mf.xc = 'pbesol'
print(mf.with_df)
mf.kernel()

molden.from_mo(cell, 'co2_crystal_deloc.molden', mf.mo_coeff)

# Orbital energies, Mulliken population etc.
mf.analyze()

# Prepare the matrix that takes care of overlap
s1e = mf.get_ovlp() 
x = np.linalg.inv(scipy.linalg.sqrtm(s1e))

# ham_orth is the Hamiltonian matrix in the AO basis,
# but it's an *orthonormalized* AO basis
# Can ignore overlap after this
ham_ao = mf.get_hcore() + mf.get_veff()
ham_orth = np.dot(x.T, np.dot(ham_ao, x))

# Test that you get back the KS eigenvalues
evals, evecs = np.linalg.eigh(ham_orth)
print(evals)

'''
nao, _ = ham_orth.shape

e1, v1 = np.linalg.eigh(ham_orth[:nao//2,:nao//2])
e2, v2 = np.linalg.eigh(ham_orth[nao//2:,nao//2:])

print("Molecule 1 MOs")
print("**************")
for i, ei in enumerate(e1):
    print(i, ei)

print("Molecule 2 MOs")
print("**************")
for i, ei in enumerate(e2):
    print(i, ei)

# Transform the Hamiltonian into the basis of molecular orbitals (MOs)
v = np.block([[v1, v1*0], [v2*0, v2]])
ham_mol_mo = np.dot(v.T, np.dot(ham_orth, v))

#c_loc_orth = lo.orth.orth_ao(mol)
molden.from_mo(cell, 'co2_dimer.molden', np.dot(x,v))

homo = cell.nelectron//2 - 1
homo1 = homo//2
homo2 = nao//2 + homo1

print(f"nao = {nao}")
print(f"HOMO1 = {homo1}")
print(f"HOMO2 = {homo2}")
for i in range(nao//2):
    for j in range(nao//2, nao):
        if ham_mol_mo[i,j] > 1e-3:
            print(f"({i+1},{j+1}) : {ham_mol_mo[i,j]}")
            #print(f"({i},{j-nao//2}) : {ham_mol_mo[i,j]}")

#10,11 w/ 25,26

ham_mol_mo *= 27.21139
print("HOMO/HOMO =", ham_mol_mo[homo1,homo2])
print("HOMO-1/HOMO =", ham_mol_mo[homo1-1,homo2])
print("HOMO/HOMO-1 =", ham_mol_mo[homo1,homo2-1])
print("HOMO-1/HOMO-1 =", ham_mol_mo[homo1-1,homo2-1])
'''
