import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

meandensity_H1x = np.loadtxt('./data/fig5d/meandensity_H1x.csv', delimiter=",")
meandensity_H1y = np.loadtxt('./data/fig5d/meandensity_H1y.csv', delimiter=",")
meandensity_H2x = np.loadtxt('./data/fig5d/meandensity_H2x.csv', delimiter=",")
meandensity_H2y = np.loadtxt('./data/fig5d/meandensity_H2y.csv', delimiter=",")

meandensityH1 = meandensity_H1x + meandensity_H1y
meandensityH1[meandensityH1 > 10**-3] = 2
meandensityH1[meandensityH1 < 10**-3] = 1

for i in range(len(meandensityH1)):
    for j in range(len(meandensityH1[i])):
        if i > 50 and i < 65:
            meandensityH1[i][j] = 2

meandensityH2 = meandensity_H2x + meandensity_H2y
meandensityH2[meandensityH2 < 10**-3] = 0
meandensityH2[meandensityH2 > 0] = 3

for i in range(len(meandensityH2)):
    for j in range(len(meandensityH2[i])):
        if i < 50 and j > 65:
            meandensityH2[i][j] = 3

for i in range(len(meandensityH2)):
    for j in range(len(meandensityH2[i])):
        if i > 50 and i < 65:
            meandensityH2[i][j] = 3

# masking
meandensity = meandensityH1 + meandensityH2
meandensity[meandensity == 2] = 1
meandensity[meandensity == 5] = 2
meandensity[meandensity == 4] = 3
meandensity1 = meandensity
meandensity1[0:47, 76:100] = np.where(meandensity1[0:47, 76:100] == 2, 0, meandensity1[0:47, 76:100]) 
mask1 = ma.masked_where(meandensity1 != 0, meandensity1)

meandensity = meandensityH1 + meandensityH2
meandensity[meandensity == 2] = 1
meandensity[meandensity == 5] = 2
meandensity[meandensity == 4] = 3
meandensity2 = meandensity
meandensity2[75:100, 0:48] = np.where(meandensity2[75:100, 0:48] == 2, 0, meandensity2[75:100, 0:48]) 
mask2 = ma.masked_where(meandensity2 != 0, meandensity2)

meandensity = meandensityH1 + meandensityH2
meandensity[meandensity == 2] = 1
meandensity[meandensity == 5] = 2
meandensity[meandensity == 4] = 3
meandensity3 = meandensity
meandensity3[73:100, 74:100] = np.where(meandensity3[73:100, 74:100] < 5, 0, meandensity3[73:100, 74:100])
mask3 = ma.masked_where(meandensity3 != 0, meandensity3)

d_Hmax_range = np.geomspace(10**-4, 10**1, 100)
meandensity = meandensityH1 + meandensityH2
meandensity[meandensity == 2] = 1
meandensity[meandensity == 5] = 2
meandensity[meandensity == 4] = 3

fig, ax = plt.subplots(figsize = (7.49,6))
im = plt.contourf(meandensity, cmap="BrBG", levels=np.linspace(1, 3, 4))
cbar = fig.colorbar(im, ticks=[1.33, 2, 2.65])
cbar.ax.set_yticklabels(['H1 superior', 'Coexistence', 'H2 superior'], fontsize=16, rotation=-40)
ax.set_xticks(np.linspace(0, len(d_Hmax_range)-1, 6))
ax.set_yticks(np.linspace(0, len(d_Hmax_range)-1, 6))
ax.set_xticklabels(["$10^{-4}$", "$10^{-3}$", "$10^{-2}$",
                    "$10^{-1}$", "$10^{0}$", "$10^{1}$"], rotation=0, fontsize=14)
ax.set_yticklabels(
    ["$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$", "$10^{1}$"], fontsize=14)
ax.set_xlabel('maximal dispersal rate $d_{max, H1}$', fontsize = 20)
ax.set_ylabel('maximal dispersal rate $d_{max, H2}$', fontsize = 20)

plt.contourf(mask1, hatches=['///'], colors='none')
plt.contourf(mask2, hatches=['///'], colors='none')
plt.contourf(mask3, hatches=['.'], colors='none')

plt.tight_layout()
plt.show()
fig.savefig('./figures/fig5f.png', dpi=300)