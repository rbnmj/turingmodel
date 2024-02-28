import numpy as np
import matplotlib.pyplot as plt

slopeH2 = np.loadtxt('./data/fig8d/H2Slope.csv', delimiter=",")
slopeH2[slopeH2 <= -0.001] = -1
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if (slopeH2[i][j] != -1) and (slopeH2[i][j] < 0.001) and (slopeH2[i][j] > -0.001):
            slopeH2[i][j] = 0
for i in range(len(slopeH2)):
    for j in range(len(slopeH2[i])):
        if ((slopeH2[i][j] >= 0.001)):
            slopeH2[i][j] = 1

fig, ax = plt.subplots(figsize=(8, 8))
im = plt.contourf(slopeH2, cmap="BrBG", levels=np.linspace(-1, 1, 4))
cbar = fig.colorbar(im)
cbar.set_ticks([-1, 0, 1])
cbar.set_label('invasion fitness $F_{mut}$', rotation=270, labelpad=18, fontsize=20)
cbar.set_ticklabels(["$-$","$0$","$+$"], fontsize=16)
#plt.plot([0, 99], [0, 99], color="black", linestyle="--", linewidth=0.5, alpha = 0.5)
ax.set_xticks(np.linspace(0, 99, 3))
ax.set_yticks(np.linspace(0, 99, 3))
ax.set_xticklabels(("$10^{-2}$", "$10^{-1}$", "$10^{0}$"), rotation=0, fontsize=16)
ax.set_yticklabels(("$10^{-2}$", "$10^{-1}$", "$10^{0}$"), fontsize=16)
ax.set_xlabel('sensitivity of the resident $k_{res}$', fontsize=20)
ax.set_ylabel('sensitivity of the mutant $k_{mut}$', fontsize=20)
ax.set_title("$d_{max} = 10^{0}$", fontsize=20)
plt.axis('square')

#y=94
#x=33
# draw start at position 33,94 on the heatmap
plt.plot(50, 94, "D", color="black", markersize=10)

plt.savefig('./figures/fig8f.png', dpi=300)
plt.show()