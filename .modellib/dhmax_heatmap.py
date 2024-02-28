import numpy as np
from scipy import integrate as integ
from matplotlib import pyplot as plt
from scipy import signal as signal
import seaborn as sns
from tqdm import tqdm
import sys
sys.path.append('./')
from turing_model import TuringModel as tm

var = []
k_1 = 0
k_2 = 0
d_Hmax1 = 0
d_Hmax2 = 0

d_Hmax_range = np.geomspace(10**-4, 10**1, 100)
var_ini = [2, 2.5, 2.5, 2, 0.8, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Save results
# results = np.zeros((len(d_Hmax1_range),len(d_Hmax2_range)))
density_H1x = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
density_H1y = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
density_H2x = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
density_H2y = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
mode_H1 = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
mode_H2 = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
checkOsc_H1x = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
checkOsc_H1y = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
checkOsc_H2x = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
checkOsc_H2y = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
meandensity_H1x = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
meandensity_H1y = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
meandensity_H2x = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
meandensity_H2y = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
autodensity_Ax = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
autodensity_Ay = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
autodensityOsc_Ax = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))
autodensityOsc_Ay = np.zeros(((len(d_Hmax_range)),(len(d_Hmax_range))))

# save initial values in an array
initials = np.array(var_ini)

save_lib = {
    "checkOsc_H1x": checkOsc_H1x,
    "checkOsc_H1y": checkOsc_H1y,
    "checkOsc_H2x": checkOsc_H2x,
    "checkOsc_H2y": checkOsc_H2y,
    "meandensity_H1x": meandensity_H1x,
    "meandensity_H1y": meandensity_H1y,
    "meandensity_H2x": meandensity_H2x,
    "meandensity_H2y": meandensity_H2y,
    "autodensity_Ax": autodensity_Ax,
    "autodensity_Ay": autodensity_Ay,
    "autodensityOsc_Ax": autodensityOsc_Ax,
    "autodensityOsc_Ay": autodensityOsc_Ay,
    "initials": initials
}


# Integrating over two variable parameters

t_ini_end = 5000
number_steps = 5000
t_ini = np.linspace(0, t_ini_end, number_steps)

t_end = 50000
number_steps = 50000
t = np.linspace(0, t_end, number_steps)

var = []

i = 0
j = 0

for d_Hmax2 in tqdm(d_Hmax_range):
    j = 0
    for d_Hmax1 in d_Hmax_range:
        model_ini = tm(var_ini, t_ini, k_1, k_2, d_Hmax1, d_Hmax2)
        var = integ.odeint(tm.equations_wrapper, var_ini, t_ini, args=(model_ini,))
        var0 = [var[-1,0], var[-1,1], var[-1,2], var[-1,3], 0.5*var[-1,4], 0.5*var[-1,5], 0.5*var[-1,4], 0.5*var[-1,5], 0, 0, 0, 0, 0, 0, 0, 0]
        model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
        var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))

        # results[i,j] = ...
        checkOsc_H1x[i, j] = np.var(var[-1000:-1, 4])
        checkOsc_H1y[i, j] = np.var(var[-1000:-1, 5])
        checkOsc_H2x[i, j] = np.var(var[-1000:-1, 6])
        checkOsc_H2y[i, j] = np.var(var[-1000:-1, 7])

        meandensity_H1x[i, j] = np.mean(var[-1000:-1, 4])
        meandensity_H1y[i, j] = np.mean(var[-1000:-1, 5])
        meandensity_H2x[i, j] = np.mean(var[-1000:-1, 6])
        meandensity_H2y[i, j] = np.mean(var[-1000:-1, 7])

        autodensity_Ax[i, j] = np.mean(var[-1000:-1, 2])
        autodensity_Ay[i, j] = np.mean(var[-1000:-1, 3])

        autodensityOsc_Ax[i, j] = np.var(var[-1000:-1, 2])
        autodensityOsc_Ay[i, j] = np.var(var[-1000:-1, 3])

        j += 1
    i += 1

tm.savedata("01_dhmax-new/k1equalsk2", save_lib)


# Random dispersal scenario
# Heatmap: Iterating over dHmax1 and dHmax2 for k1 = k2 = 0.
ld = tm.loaddata("01_dhmax-new/k1equalsk2", ["meandensity_H1x", "meandensity_H2x"])
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 8), gridspec_kw={'top': 1.25})

sns.heatmap(ld["meandensity_H1x"], cmap="viridis",
            square=True, cbar=False, ax=ax1, vmin=0, vmax=np.max(ld["meandensity_H1x"]))
ax1.set_ylabel("Maximal dispersal rate $d_{H_{max2}}$", fontsize=14)
ax1.invert_yaxis()
ax1.set_xticks(np.linspace(0, len(d_Hmax_range), 6))
ax1.set_xticklabels(["$10^{-4}$", "$10^{-3}$", "$10^{-2}$",
                    "$10^{-1}$", "$10^{0}$", "$10^{1}$"], rotation=0)
ax1.set_yticks(np.linspace(0, len(d_Hmax_range), 6))
ax1.set_yticklabels(
    ["$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$", "$10^{1}$"])
ax1.set_title("H1", fontsize=14)

sns.heatmap(ld["meandensity_H2x"], cmap="viridis",
            square=True, cbar=False, ax=ax2, vmin=0, vmax=np.max(ld["meandensity_H1x"]))
ax2.invert_yaxis()
ax2.set_xticks(np.linspace(0, len(d_Hmax_range), 6))
ax2.set_xticklabels(["$10^{-4}$", "$10^{-3}$", "$10^{-2}$",
                    "$10^{-1}$", "$10^{0}$", "$10^{1}$"], rotation=0)
ax2.set_yticks(np.linspace(0, len(d_Hmax_range), 6))
ax2.set_title("H2", fontsize=14)

fig.text(
    0.55, 0.42, 'Maximal dispersal rate $d_{H_{max1}}$', ha='center', fontsize=14)
fig.subplots_adjust(right=0.95)
cb_ax = fig.add_axes([0.99, 0.493, 0.02, 0.377])
cbar = fig.colorbar(ax1.get_children()[0], cax=cb_ax)
fig.suptitle(
    "Random dispersal scenario: $k_1 = k_2 = 0$. \n Mean densities of $H1$ and $H2$ on patch $x$")
fig.tight_layout()
plt.savefig("./output/01_dhmax-new/k1equalsk2/k1equalsk2_autoheatmap.png")
plt.show()
