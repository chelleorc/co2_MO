import numpy as np
import scipy
import pyscf
from pyscf import gto, dft
from pyscf.tools import molden

'''
CO2 dimer
'''

mol = gto.Mole()
mol.atom = '''
O          3.42213        7.57202        4.82348
C          2.74854        8.24561        5.49707
O          2.07494        8.91920        6.17067
O          4.82348        4.82348        4.82348
C          5.49707        5.49707        5.49707
O          6.17067        6.17067        6.17067
'''
mol.basis = 'sto6g'
mol.build()

mf = dft.RKS(mol)
mf.xc = 'pbe'
mf.kernel()

molden.from_mo(mol, 'co2_dimer_deloc.molden', mf.mo_coeff)

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
# evals, evecs = np.linalg.eigh(ham_orth)
# print(evals)

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
molden.from_mo(mol, 'co2_dimer.molden', np.dot(x,v))

homo = mol.nelectron//2 - 1
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
