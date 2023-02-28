import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# import csv


    
'''
Main
'''

# column_names = ["Energy Cutoff", "Total Energy", "Wall Time"]

column_names = ["K Points","Total Energy","Wall Time"]

file = pd.read_csv('/mnt/home/landerson1/projects/tight_binding/wannier90/co2_MO/convergence_test/_data/co2_kpoints.csv',sep=',')

df = pd.DataFrame(file.to_numpy(), columns=column_names)

# energy_cutoff=df["Energy Cutoff"]
total_energy=df["Total Energy"]
k_points=df["K Points"]
wall_time=df["Wall Time"]

# plt.plot(energy_cutoff,total_energy)
plt.plot(k_points,total_energy)

# Save figure by renaming to atom of interest
plt.savefig('plot/kpoints.png')

plt.show()