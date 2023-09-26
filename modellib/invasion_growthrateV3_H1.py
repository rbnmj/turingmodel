# this version is mostly identical to V3 
# but instead is looking the the last ten maxima of H1 to understand
# the long term growth or decay after the invasion attempt of H2.
import numpy as np
import sympy as sp
import matplotlib
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
import seaborn as sns
###


# running sim
from scipy.stats import linregress
import ipywidgets
from tqdm import tqdm
from scipy import integrate as integ
from scipy import signal as signal
import sys
sys.path.append('./')
from turing_model import TuringModel as tm

def find_maxima(x,n):
    """ returns an array with n extreme values of x"""
    
    max_index = signal.argrelmax(x)[0]         # create array with indices of local maxima of x
    
    #ext_index = np.append(max_index)           # array with indices of local extrema in x
    #ext_index = np.sort(ext_index)             # sort array (alternating minima and maxima)
    extrema = x[max_index]                     # array with the actual values of the extrema
       
    if len(extrema) == 0:                      # if all values in x are the same and no extremum is found:
        extrema = np.append(extrema,x[-1])     #   return last value of x in this case
    while len(extrema) < n:                    # if less than n extrema have been found:
        extrema = np.append(extrema,extrema[0])#   repeat last extremum until array has n elements
    while len(extrema) > n:                    # if more than n extrema have been found:
        extrema = np.delete(extrema,-1)        #   delete elements until arrays has n elements
        
    return extrema

t_end = 10000 
number_steps = 10000 
t = np.linspace(0, t_end, number_steps)

# dispersal adaptability
k_1_range = np.geomspace(0.1, 10, 50)
k_2_range = np.geomspace(0.1, 10, 50)

# maximum dispersal rate
d_Hmax1 = 10**-3
d_Hmax2 = 10**-3

# var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 10**-6, 0, 0, 0, 0, 0, 0, 0]

num_extr = 200 # set number of maxima to be found

H1_extr = []
H2_extr = []

slopeH1 = np.zeros((len(k_1_range), len(k_2_range)))
slopeH2 = np.zeros((len(k_1_range), len(k_2_range)))
var = []

i = 0
j = 0

for k_2 in tqdm(k_2_range):
    j = 0
    for k_1 in k_1_range:
        model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
        var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))

        H1_extr.append(find_maxima(var[:, 4]+var[:, 5],num_extr))
        H2_extr.append(find_maxima(var[:, 6]+var[:, 6],num_extr))

        # remove duplicates (e.g. if not enough maxima are found)
        H1_extr = np.unique(H1_extr)
        H2_extr = np.unique(H2_extr)

        # save last 20 maxima
        H1_extr = H1_extr[-10:]
        H2_extr = H2_extr[-10:]

        # results[i,j] = ...
        slopeH1[i, j] = linregress(np.linspace(0, 9, 10),H1_extr)[0]
        slopeH2[i, j] = linregress(np.linspace(0, 9, 10),H2_extr)[0]

        # workaround to empty lists
        H1_extr = []
        H2_extr = []

        j += 1
    i += 1

# saving results
np.savetxt("./data/growthrateV3_H1_10-3/H1Slope10-2.csv", slopeH1, delimiter=",")
np.savetxt("./data/growthrateV3_H1_10-3/H2Slope10-2.csv", slopeH2, delimiter=",")

# # loading results
# H1a = np.loadtxt("./data/growthrateV210-3/H1a10k.csv", delimiter=",")
# H1b = np.loadtxt("./data/growthrateV210-3/H1b10k.csv", delimiter=",")
# H2a = np.loadtxt("./data/growthrateV210-3/H2a10k.csv", delimiter=",")
# H2b = np.loadtxt("./data/growthrateV210-3/H2b10k.csv", delimiter=",")

d_Hmax = "10-3"

# plotting
k_1_range = np.geomspace(0.1, 10, 50)
ticks = np.append(k_1_range, 10)

# total change
fig, ax1 = plt.subplots()
ax1 = sns.heatmap((slopeH1-slopeH2), cmap="BrBG", square=True, cbar=False)#, vmin=-10**-7, vmax=10**-7)
cbar1 = ax1.figure.colorbar(ax1.collections[0])
cbar1.set_label('$H_1 - H_2$', rotation=270, labelpad=12)
ax1.set_xticks(np.linspace(0, len(k_1_range), 3))
ax1.set_yticks(np.linspace(0, len(k_1_range), 3))
ax1.invert_yaxis()
ax1.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0)
ax1.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"))
plt.grid(color='black', linewidth=0.5, linestyle='--')
plt.xlabel('$k_1$')
plt.ylabel('$k_2$')
plt.title(
    'Change of heterotroph densitiy \n $d_{H_{max}} = $' + str(d_Hmax) + ', H2 invader')
plt.savefig('./output/invasion_growthrateV3_H1_'+str(d_Hmax)+'_H1-H2.png')

# H1 change
fig, ax2 = plt.subplots()
k_1_range = np.geomspace(0.1, 10, 50)
ticks = np.append(k_1_range, 10)
ax2 = sns.heatmap((slopeH1), cmap="BrBG", square=True, cbar=False)#, vmin=-10**-7, vmax=10**-7)
cbar2 = ax2.figure.colorbar(ax2.collections[0])
cbar2.set_label('$H_1$', rotation=270, labelpad=12)
ax2.set_xticks(np.linspace(0, len(k_1_range), 3))
ax2.set_yticks(np.linspace(0, len(k_1_range), 3))
ax2.invert_yaxis()
ax2.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0)
ax2.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"))
plt.grid(color='black', linewidth=0.5, linestyle='--')
plt.xlabel('$k_1$')
plt.ylabel('$k_2$')
plt.title('Growth rate of $H_1$ \n $d_{H_{max}} = $' + str(d_Hmax) + ', H2 invader')
plt.savefig('./output/invasion_growthrateV3_H1_'+str(d_Hmax)+'_H1.png')

# H2 change
fig, ax3 = plt.subplots()
k_1_range = np.geomspace(0.1, 10, 50)
ticks = np.append(k_1_range, 10)
ax3 = sns.heatmap((slopeH2), cmap="BrBG", square=True, cbar=False)#, vmin=-10**-9, vmax=10**-9)
cbar3 = ax3.figure.colorbar(ax3.collections[0])
cbar3.set_label('$H_2$', rotation=270, labelpad=12)
ax3.set_xticks(np.linspace(0, len(k_1_range), 3))
ax3.set_yticks(np.linspace(0, len(k_1_range), 3))
ax3.invert_yaxis()
ax3.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0)
ax3.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"))
plt.grid(color='black', linewidth=0.5, linestyle='--')
plt.xlabel('$k_1$')
plt.ylabel('$k_2$')
plt.title('Growth rate of $H_2$ \n $d_{H_{max}} = $' + str(d_Hmax) + ', H2 invader')
plt.savefig('./output/invasion_growthrateV3_H1_'+str(d_Hmax)+'_H2.png')