import numpy as np
import sympy as sp
import matplotlib
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
import seaborn as sns
###


# # running sim
# from scipy.stats import linregress
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
#         #invasion[i, j] = total_H1[i, j] - total_H2[i, j]

#         slope, intercept, r_value, p_value, std_err = linregress(t[-200:-1],var[-200:-1, 4])
#         H1a[i, j] = slope
#         slope, intercept, r_value, p_value, std_err = linregress(t[-200:-1],var[-200:-1, 5])
#         H1b[i, j] = slope
#         slope, intercept, r_value, p_value, std_err = linregress(t[-200:-1],var[-200:-1, 6])
#         H2a[i, j] = slope
#         slope, intercept, r_value, p_value, std_err = linregress(t[-200:-1],var[-200:-1, 7])
#         H2b[i, j] = slope
#         j += 1
#     i += 1

# loading results
H1a = np.loadtxt("./data/growthrate10-3/H1a.csv", delimiter=",")
H1b = np.loadtxt("./data/growthrate10-3/H1b.csv", delimiter=",")
H2a = np.loadtxt("./data/growthrate10-3/H2a.csv", delimiter=",")
H2b = np.loadtxt("./data/growthrate10-3/H2b.csv", delimiter=",")

d_Hmax = "10-3"

# plotting
k_1_range = np.geomspace(0.1, 10, 50)
ticks = np.append(k_1_range, 10)

# total change
fig, ax1 = plt.subplots()
ax1 = sns.heatmap((H1a+H1b)-(H2a+H2b), cmap="viridis", square=True, cbar=False)
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
plt.savefig('./output/invasion_growthrate_'+str(d_Hmax)+'_H1-H2.png')

# H1 change
fig, ax2 = plt.subplots()
k_1_range = np.geomspace(0.1, 10, 50)
ticks = np.append(k_1_range, 10)
ax2 = sns.heatmap((H1b+H1a), cmap="viridis", square=True, cbar=False)
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
plt.savefig('./output/invasion_growthrate_'+str(d_Hmax)+'_H1.png')

# H2 change
fig, ax3 = plt.subplots()
k_1_range = np.geomspace(0.1, 10, 50)
ticks = np.append(k_1_range, 10)
ax3 = sns.heatmap((H2b+H2a), cmap="viridis", square=True, cbar=False)
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
plt.savefig('./output/invasion_growthrate_'+str(d_Hmax)+'_H2.png')