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

t_end = 20000 
number_steps = 20000 
t = np.linspace(0, t_end, number_steps)

# dispersal adaptability
k_1_range = np.geomspace(0.1, 10, 50)#100)
k_2_range = np.geomspace(0.1, 10, 50)#100)

# maximum dispersal rate
d_Hmax1 = 10**0
d_Hmax2 = 10**0

# var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 10**-6, 0, 0, 0, 0, 0, 0, 0]

num_extr = 40 # set number of maxima to be found

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

        H1_extr.append(find_maxima(np.log(var[:, 4])+np.log(var[:, 5]),num_extr))
        H2_extr.append(find_maxima(np.log(var[:, 6])+np.log(var[:, 6]),num_extr))

        # results[i,j] = ...
        slopeH1[i, j] = linregress(np.linspace(1, 20, 20),H1_extr[0][20:num_extr])[0]
        slopeH2[i, j] = linregress(np.linspace(1, 20, 20),H2_extr[0][20:num_extr])[0]

        # workaround to empty lists
        H1_extr = []
        H2_extr = []

        j += 1
    i += 1

# saving results
np.savetxt("./data/growthrate/100/H1Slope10-0.csv", slopeH1, delimiter=",")
np.savetxt("./data/growthrate/100/H2Slope10-0.csv", slopeH2, delimiter=",")

# # loading results
# slopeH1 = np.loadtxt("./data/growthrateV3_10-3/H1Slope10-3_logV2.csv", delimiter=",")
# slopeH2 = np.loadtxt("./data/growthrateV3_10-3/H2Slope10-3_logV2.csv", delimiter=",")

d_Hmax = "10-0"

# plotting
k_1_range = np.geomspace(0.1, 10, 50)
ticks = np.append(k_1_range, 10)

# # total change
# fig, ax1 = plt.subplots()
# ax1 = sns.heatmap((slopeH1-slopeH2), cmap="BrBG", square=True, cbar=False)
# cbar1 = ax1.figure.colorbar(ax1.collections[0])
# cbar1.set_label('$H_1 - H_2$', rotation=270, labelpad=12)
# ax1.set_xticks(np.linspace(0, len(k_1_range), 3))
# ax1.set_yticks(np.linsace(0, len(k_1_range), 3))
# ax1.invert_yaxis()
# ax1.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0)
# ax1.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"))
# plt.grid(color='black', linewidth=0.5, linestyle='--')
# plt.xlabel('$k_1$')
# plt.ylabel('$k_2$')
# plt.title(
#     'Change of heterotroph densitiy \n $d_{H_{max}} = $' + str(d_Hmax) + ', H2 invader')
# plt.savefig('./output/final/invasion_growthrateV3_'+str(d_Hmax)+'_H1-H2_logV2.png')

# H1 change
fig, ax2 = plt.subplots()
k_1_range = np.geomspace(0.1, 10, 100)
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
plt.savefig('./output/final/invasion_growthrateV3_'+str(d_Hmax)+'_H1_logV2.png')

# H2 change
fig, ax3 = plt.subplots()
k_1_range = np.geomspace(0.1, 10, 100)
ticks = np.append(k_1_range, 10)
ax3 = sns.heatmap((slopeH2), cmap="BrBG", square=True, cbar=False, vmin=-0.04, vmax=0.04)
cbar3 = ax3.figure.colorbar(ax3.collections[0])
cbar3.set_label('$H_2$', rotation=270, labelpad=12)
ax3.set_xticks(np.linspace(0, len(k_1_range), 3))
ax3.set_yticks(np.linspace(0, len(k_1_range), 3))
ax3.invert_yaxis()
ax3.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0)
ax3.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"))
#plt.grid(color='black', linewidth=0.5, linestyle='--')
ax3.plot([0, len(k_1_range)], [0, len(k_1_range)], color="black", linestyle="--", linewidth=0.75)
plt.xlabel('$k_1$')
plt.ylabel('$k_2$')
plt.title('Growth rate of $H_2$ \n $d_{H_{max}} = $' + str(d_Hmax) + ', H2 invader')
plt.savefig('./output/final/invasion_growthrateV3_'+str(d_Hmax)+'_H2_logV2.png')

# H2 change "binary"
slopeH2[slopeH2 <= -0.00005] = -1
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if (slopeH2[i][j] != -1) and (slopeH2[i][j] < 0.00005) and (slopeH2[i][j] > -0.00005):
            slopeH2[i][j] = 0
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if ((slopeH2[i][j] >= 0.00005)):
            slopeH2[i][j] = 1

fig, ax = plt.subplots()
im = plt.contourf(slopeH2, cmap="PuOr", levels=np.linspace(-1, 1, 4), alpha=0.8)
cbar = fig.colorbar(im)
cbar.set_ticks([-1, 0, 1])
cbar.set_label('Invader growth', rotation=270, labelpad=12)
plt.plot([0, 99], [0, 99], color="black", linestyle="--", linewidth=0.5, alpha = 0.5)
ax.set_xticks(np.linspace(0, 99, 3))
ax.set_yticks(np.linspace(0, 99, 3))
ax.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0)
ax.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"))
ax.set_xlabel('$k_1$')
ax.set_ylabel('$k_2$')
plt.title('Growth rate of $H_2$ \n $d_{H_{max}} = $' + str(d_Hmax) + ', H2 invader')
plt.savefig('./output/final/invasion_growthrateV3_'+str(d_Hmax)+'_H2_logV2_binary.png')