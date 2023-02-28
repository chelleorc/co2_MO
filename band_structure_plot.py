import matplotlib.pyplot as plt
from matplotlib import rcParamsDefault
import numpy as np
import subprocess as sp
# set new figure defaults
plt.rcParams["figure.dpi"]=150
plt.rcParams["figure.facecolor"]="white"
plt.rcParams["figure.figsize"]=(8, 6)
plt.rcParams['font.size'] = 18

# load band structure data
data = np.loadtxt('/mnt/home/landerson1/projects/tight_binding/wannier90/co2_MO/_data/CO2.bands.dat.gnu')

# find the unique array elements of the first column and initialize k
k = np.unique(data[:, 0])


# Reshape data into a list of lists
# bands = np.reshape(data[:, 1]-10.3416, (-1, len(k)))
bands = np.reshape(data[:, 1], (-1, len(k)))
# print(type(bands))
bands_corrected = bands

# Iterate through band structure data where x = k and y = bands[bands, :]
for band in range(len(bands)):
    plt.plot(k, bands[band, :], linewidth=1, alpha=0.5, color='g')

# for band in range(len(bands)):
#     # if bands[band, :]:
#         upper_bands = bands[band, :] > 0
#         print(upper_bands)
#         # plt.plot(k, upper_bands[band,], linewidth=1, alpha=0.5, color='k')

# set minimum and maximum x chart limits
plt.xlim(min(k), max(k))
plt.ylim(-5.0, 8.5)


'''
If system is a metal, set Fermi energy level by using bash command:
    grep 'Fermi energy' bands_x_calc_file.out
'''
# plt.axhline(0.0000, linestyle=(0, (5, 5)), linewidth=0.75, color='k', alpha=0.5)

plt.axvline(0.0000, linewidth=0.75, color='k', alpha=0.5) #G
plt.axvline(0.8082, linewidth=0.75, color='k', alpha=0.5) #M
plt.axvline(1.3797, linewidth=0.75, color='k', alpha=0.5) #R
plt.axvline(2.1880, linewidth=0.75, color='k', alpha=0.5) #X
plt.axvline(2.9962, linewidth=0.75, color='k', alpha=0.5) #X1

# plt.axvline(0.0000, linewidth=0.75, color='k', alpha=0.5) #G
# plt.axvline(0.4067, linewidth=0.75, color='k', alpha=0.5) #Z
# plt.axvline(0.9172, linewidth=0.75, color='k', alpha=0.5) #T
# plt.axvline(1.3239, linewidth=0.75, color='k', alpha=0.5) #R
# plt.axvline(1.8753, linewidth=0.75, color='k', alpha=0.5) #V
# plt.axvline(2.3857, linewidth=0.75, color='k', alpha=0.5) #X
# plt.axvline(2.9372, linewidth=0.75, color='k', alpha=0.5) #G


# plt.axhline(10.3416, linewidth=0.75, color='k', alpha=0.5) # Fermi level


# text labels and ticks at each high symmetry point on x-axis
plt.xticks(ticks= [0.0000,0.8082,1.3797,2.1880,2.9962], \
           labels=['$\Gamma$','M','R','X','X1'])
# plt.xticks(ticks= [0.0000,0.4067,0.9172, 1.3239,1.8753, 2.3857, 2.9372], \
        #    labels=['$\Gamma$','Z','T','R','V','X','$\Gamma$'])
plt.ylabel("Energy (eV)")


# save file as png
plt.savefig('plot/qe_band_structure.png')
plt.show()