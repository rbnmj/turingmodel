import numpy as np
import matplotlib.pyplot as plt

# dhmax = 10^-3
slopeH2 = np.loadtxt("./data/fig7d/H2Slope10-3.csv", delimiter=",")
slopeH2[slopeH2 <= -0.00005] = -1
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if (slopeH2[i][j] != -1) and (slopeH2[i][j] < 0.00005) and (slopeH2[i][j] > -0.00005):
            slopeH2[i][j] = 0
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if ((slopeH2[i][j] >= 0.00005)):
            slopeH2[i][j] = 1

fig, ax = plt.subplots(figsize=(8, 8))
im = plt.contourf(slopeH2, cmap="BrBG", levels=np.linspace(-1, 1, 4))#, alpha=0.8)
cbar = fig.colorbar(im)
cbar.set_ticks([-0.66, 0, 0.66])
cbar.set_ticklabels(["$-$","$0$","$+$"], fontsize=16)
cbar.set_label('invasion fitness $F_{mut}$', rotation=270, labelpad=25, fontsize=20)
plt.plot([0, 99], [0, 99], color="black", linestyle="--", linewidth=0.5, alpha = 0.5)
ax.set_xticks(np.linspace(0, 99, 3))
ax.set_yticks(np.linspace(0, 99, 3))
ax.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0, fontsize=16)
ax.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), fontsize=16)
ax.set_xlabel('sensitivity of the resident $k_{res}$', fontsize=20)
ax.set_ylabel('sensitivity of the mutant $k_{mut}$', fontsize=20)
ax.set_title("$d_{max} = 10^{-3}$", fontsize=20)
plt.axis('square')
plt.savefig('./figures/fig7af.png', dpi=300)

# dhmax = 5*10^-3
slopeH2 = np.loadtxt("./data/fig7d/H2Slope510-3.csv", delimiter=",")
slopeH2[slopeH2 <= -0.00005] = -1
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if (slopeH2[i][j] != -1) and (slopeH2[i][j] < 0.00005) and (slopeH2[i][j] > -0.00005):
            slopeH2[i][j] = 0
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if ((slopeH2[i][j] >= 0.00005)):
            slopeH2[i][j] = 1

fig, ax = plt.subplots(figsize=(8, 8))
im = plt.contourf(slopeH2, cmap="BrBG", levels=np.linspace(-1, 1, 4))
cbar = fig.colorbar(im)
cbar.set_ticks([-0.66, 0, 0.66])
cbar.set_ticklabels(["$-$","$0$","$+$"], fontsize=16)
cbar.set_label('invasion fitness $F_{mut}$', rotation=270, labelpad=25, fontsize=20)
cbar.ax.tick_params(size=0)
ax.set_xticks(np.linspace(0, 99, 3))
ax.set_yticks(np.linspace(0, 99, 3))
ax.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0, fontsize=16)
ax.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), fontsize=16)
ax.set_xlabel('sensitivity of the resident $k_{res}$', fontsize=20)
ax.set_ylabel('sensitivity of the mutant $k_{mut}$', fontsize=20)
ax.set_title("$d_{max} = 5 \cdot 10^{-3}$", fontsize=20)
plt.axis('square')
plt.savefig('./figures/fig7bf.png', dpi=300)

# dmax = 10^-2
slopeH2 = np.loadtxt("./data/fig7d/H2Slope10-2.csv", delimiter=",")
slopeH2[slopeH2 <= -0.00005] = -1
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if (slopeH2[i][j] != -1) and (slopeH2[i][j] < 0.00005) and (slopeH2[i][j] > -0.00005):
            slopeH2[i][j] = 0
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if ((slopeH2[i][j] >= 0.00005)):
            slopeH2[i][j] = 1

fig, ax = plt.subplots(figsize=(8, 8))
im = plt.contourf(slopeH2, cmap="BrBG", levels=np.linspace(-1, 1, 4))
cbar = fig.colorbar(im)
cbar.set_ticks([-0.66, 0, 0.66])
cbar.set_ticklabels(["$-$","$0$","$+$"], fontsize=16)
cbar.set_label('invasion fitness $F_{mut}$', rotation=270, labelpad=25, fontsize=20)
ax.set_xticks(np.linspace(0, 49, 3))
ax.set_yticks(np.linspace(0, 49, 3))
ax.set_xticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), rotation=0, fontsize=16)
ax.set_yticklabels(("$10^{-1}$", "$10^{0}$", "$10^{1}$"), fontsize=16)
ax.set_xlabel('sensitivity of the resident $k_{res}$', fontsize=20)
ax.set_ylabel('sensitivity of the mutant $k_{mut}$', fontsize=20)
ax.set_title("$d_{max} = 10^{-2}$", fontsize=20)
plt.axis('square')
plt.savefig('./figures/fig7cf.png', dpi=300)

plt.show()