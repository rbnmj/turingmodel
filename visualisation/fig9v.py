import numpy as np
import matplotlib.pyplot as plt


# invasion for osc pattern
# load data
Hdiff_slope = np.load('./data/fig9d/Hdiff_slope_10-2.npy')
Hdiff_slope[Hdiff_slope <= -10**-6] = -1
for i in range(len(Hdiff_slope)):
    for j in range(len(Hdiff_slope[i])):
        if (Hdiff_slope[i][j] != -1) and (Hdiff_slope[i][j] < 10**-6) and (Hdiff_slope[i][j] > -10**-6):
            Hdiff_slope[i][j] = 0
for i in range(len(Hdiff_slope)):
    for j in range(len(Hdiff_slope[i])):
        if ((Hdiff_slope[i][j] >= 10**-6)):
            Hdiff_slope[i][j] = 1

fig, ax = plt.subplots()
im = plt.contourf(Hdiff_slope, cmap="BrBG", levels=np.linspace(-1, 1, 4))
cbar = fig.colorbar(im)
cbar.set_ticks([-0.66, 0, 0.66])
cbar.set_ticklabels(["$-$","$0$","$+$"], fontsize = 16)
cbar.set_label('invasion fitness $F_{mut}$', rotation=270, labelpad=18, fontsize=20)
cbar.ax.tick_params(size=0)
ax.set_xticks(np.linspace(0, 99, 5))
ax.set_yticks(np.linspace(0, 99, 5))
ax.set_xticklabels(("$10^{-2}$", "$10^{-1}$", "$10^{0}$", "$10^{1}$", "$10^{2}$"), rotation=0, fontsize=16)
ax.set_yticklabels(("$10^{-2}$", "$10^{-1}$", "$10^{0}$", "$10^{1}$", "$10^{2}$"), fontsize=16)
ax.set_xlabel('sensitivity of the resident $k_{res}$', fontsize=20)
ax.set_ylabel('sensitivity of the mutant $k_{mut}$', fontsize=20)
ax.set_title("$d_{max} = 10^{-2}$", fontsize=20)
plt.axis('square')
plt.savefig('./figures/fig9af.png', dpi=300)

# invasion for static pattern
# load data
Hdiff_slope = np.load('./data/fig9d/Hdiff_slope_10-0.npy')
Hdiff_slope[Hdiff_slope <= -10**-7] = -1
for i in range(len(Hdiff_slope)):
    for j in range(len(Hdiff_slope[i])):
        if (Hdiff_slope[i][j] != -1) and (Hdiff_slope[i][j] < 10**-7) and (Hdiff_slope[i][j] > -10**-7):
            Hdiff_slope[i][j] = 0
for i in range(len(Hdiff_slope)):
    for j in range(len(Hdiff_slope[i])):
        if ((Hdiff_slope[i][j] >= 10**-7)):
            Hdiff_slope[i][j] = 1

fig, ax = plt.subplots()
im = plt.contourf(Hdiff_slope, cmap="BrBG", levels=np.linspace(-1, 1, 4))
cbar = fig.colorbar(im)
cbar.set_ticks([-0.66, 0, 0.66])
cbar.set_ticklabels(["$-$","$0$","$+$"], fontsize=16)
cbar.set_label('invasion fitness $F_{mut}$', rotation=270, labelpad=18, fontsize=20)
cbar.ax.tick_params(size=0)
ax.set_xticks(np.linspace(0, 99, 5))
ax.set_yticks(np.linspace(0, 99, 5))
ax.set_xticklabels(("$10^{-2}$", "$10^{-1}$", "$10^{0}$", "$10^{1}$", "$10^{2}$"), rotation=0, fontsize=16)
ax.set_yticklabels(("$10^{-2}$", "$10^{-1}$", "$10^{0}$", "$10^{1}$", "$10^{2}$"), fontsize=16)
ax.set_xlabel('sensitivity of the resident $k_{res}$', fontsize=20)
ax.set_ylabel('sensitivity of the mutant $k_{mut}$', fontsize=20)
ax.set_title("$d_{max} = 10^{0}$", fontsize=20)
plt.axis('square')
plt.savefig('./figures/fig9bf.png', dpi=300)

plt.show()