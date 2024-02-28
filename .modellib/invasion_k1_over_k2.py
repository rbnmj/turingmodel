import numpy as np
from scipy import integrate as integ
from scipy import signal as signal
import sympy as sp
import matplotlib
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
import seaborn as sns
import ipywidgets
from tqdm import tqdm
###
import sys
sys.path.append('./')
from turing_model import TuringModel as tm

# # Run sim. Skip if data already exists
# t_end = 15000
# number_steps = 2000
# t = np.linspace(0, t_end, number_steps)
# # dispersal adaptability
# k_1 = 0
# k_2 = 0
# k_1_range = np.geomspace(0.1, 10, 50)
# k_2_range = np.geomspace(0.1, 10, 50)
# # maximum dispersal rate
# d_Hmax1 = 10**-2
# d_Hmax2 = 10**-2
# d_Hmax1_range = np.logspace(-3, -1, 250)
# d_Hmax2_range = k_1_range # d_Hmax1_range

# # var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
# var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 10**-6, 0, 0, 0, 0, 0, 0, 0]
# var = []
# model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)

# meandensity_H1x = np.zeros((len(d_Hmax2_range), len(d_Hmax2_range)))
# meandensity_H1y = np.zeros((len(d_Hmax2_range), len(d_Hmax2_range)))
# meandensity_H2x = np.zeros((len(d_Hmax2_range), len(d_Hmax2_range)))
# meandensity_H2y = np.zeros((len(d_Hmax2_range), len(d_Hmax2_range)))
# total_H1 = np.zeros((len(d_Hmax2_range), len(d_Hmax2_range)))
# total_H2 = np.zeros((len(d_Hmax2_range), len(d_Hmax2_range)))
# invasion = np.zeros((len(d_Hmax2_range), len(d_Hmax2_range)))

# var = []
# i = 0
# j = 0

# for k_2 in tqdm(k_2_range):
#     j = 0
#     for k_1 in k_1_range:
#         model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
#         var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))

#         # results[i,j] = ...
#         meandensity_H1x[i, j] = np.mean(var[-200:-1, 4])
#         meandensity_H1y[i, j] = np.mean(var[-200:-1, 5])
#         meandensity_H2x[i, j] = np.mean(var[-200:-1, 6])
#         meandensity_H2y[i, j] = np.mean(var[-200:-1, 7])
#         total_H1[i, j] = np.mean(var[-200:-1, 4]) + np.mean(var[-200:-1, 5])
#         total_H2[i, j] = np.mean(var[-200:-1, 6]) + np.mean(var[-200:-1, 7])
#         invasion[i, j] = total_H1[i, j] - total_H2[i, j]

#         j += 1
#     i += 1
# # save sim results
#invasion = (meandensity_H1x+meandensity_H1y) - (meandensity_H2x+meandensity_H2y)
#np.savetxt("./data/invasion10-3.csv", invasion, delimiter=",")

# # load sim results
invasion = np.loadtxt("./data/invasion10-3.csv", delimiter=",")
d_Hmax = "10-3"

# plotting 
k_1_range = np.geomspace(0.1, 10, 50)
ticks = np.append(k_1_range, 10)
ax1 = sns.heatmap(invasion, cmap="viridis", vmin=-0.4,vmax=0.4, square = True,cbar=False) # vmin=-0.4,vmax=0.4,    
cbar = ax1.figure.colorbar(ax1.collections[0])
cbar.set_label('$H_1 - H_2$', rotation=270)
ax1.set_xticks(np.linspace(0, len(k_1_range), 3))
ax1.set_yticks(np.linspace(0, len(k_1_range), 3))
ax1.invert_yaxis()
ax1.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0)
ax1.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"))
plt.grid(color='black', linewidth=0.5, linestyle='--')
plt.xlabel('$k_1$')
plt.ylabel('$k_2$')
plt.title('$d_{H_{max}} = $' + str(d_Hmax) + ', H2 invader')
plt.savefig('./output/invasion_'+str(d_Hmax)+'.png')
plt.show()


