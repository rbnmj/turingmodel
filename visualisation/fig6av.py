import numpy as np
from matplotlib import pyplot as plt

H1x = np.load('./data/fig6ad/H1x.npy')
H1y = np.load('./data/fig6ad/H1y.npy')
Htotal = H1x+H1y
im,ax = plt.subplots(figsize=(8,8))
im = ax.imshow((Htotal), cmap='inferno', aspect='auto', origin="lower")#, vmax=np.log(0.2), vmin=np.log(10**-6))
cbar = plt.colorbar(im)
cbar.set_label("density $H_1$", rotation=270, labelpad=25, fontsize=20)
cbar.ax.tick_params(labelsize=12)
ax.set_xlabel("maximal dispersal rate $d_{max, H_1}$", fontsize=20)
ax.set_ylabel("time", fontsize=20)
ax.set_xticks(np.linspace(0, 24, 6))
ax.set_xticklabels(np.linspace(4,6,6), fontsize=16)
ax.yaxis.set_tick_params(labelsize=16)
plt.title("$k = 0, d_{max,H_2} = 10^{-3}$")

plt.savefig('./figures/fig6af.png', dpi=300)
plt.show()