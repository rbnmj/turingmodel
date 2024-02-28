import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

H1osc = np.load('./data/fig1d/H1osc.npy')
H1static = np.load('./data/fig1d/H1static.npy')

fig,(ax, ax1) = plt.subplots(1,2)
im = ax.imshow(H1osc, cmap='inferno', aspect='auto', origin="lower")
ax.set_xticks(np.linspace(0, 1, 2))
ax.set_xticklabels(("Patch $x$","Patch $y$"))
ax.set_ylabel("Time")
ax.text(0.5, 1.07, "Oscillatory pattern formation", 
        fontsize='large', ha='center', va='bottom', transform=ax.transAxes)
ax.text(0.5, 1.06, "Low maximal dispersal rate", 
        fontsize='small', ha='center', va='top', transform=ax.transAxes)

im1 = ax1.imshow(H1static, cmap='inferno', aspect='auto', origin="lower")
ax1.set_xticks(np.linspace(0, 1, 2))
ax1.set_xticklabels(("Patch $x$","Patch $y$"))
ax1.set_yticklabels([])
ax1.text(0.5, 1.07, "Static pattern formation", 
        fontsize='large', ha='center', va='bottom', transform=ax1.transAxes)
ax1.text(0.5, 1.06, "High maximal dispersal rate", 
        fontsize='small', ha='center', va='top', transform=ax1.transAxes)

# cb_ax = fig.add_axes([1, 0.09, 0.02, 0.79])
# cbar didnt render: workaround with make_axes_locatable
divider = make_axes_locatable(ax1)
cb_ax = divider.append_axes('right', size='5%', pad=0.05)
cbar = fig.colorbar(ax1.get_children()[0], cax=cb_ax)
cbar.set_label('Heterotroph density', rotation=270, labelpad=-12)    
# limit cbar to 2 labels
cbar.set_ticks([0.008, 0.212])
cbar.set_ticklabels(["0", "0.25"])

# save figure
plt.savefig('./figures/fig1f.png', dpi=300)
plt.show()