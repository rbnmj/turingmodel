import numpy as np
from scipy import integrate as integ
from matplotlib import pyplot as plt
import sys
sys.path.append('./')
from turing_model import TuringModel as tm

t_end = 100000
number_steps = 1000
t = np.linspace(0, t_end, number_steps)

#var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 10**-6, 10**-6, 0, 0, 0, 0, 0, 0]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8,8))

k_1 = 0
k_2 = 5
d_Hmax1 = 10**-2
d_Hmax2 = 10**-2
var = []
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))
ax1.plot(t, (var[:, 4]),label="H1a (lower sens)", color="#FF7F0E")
ax1.plot(t, (var[:, 6]), label="H2a (higher sens)", color="#1F77B4")
ax1.plot(t, (var[:, 5]),label="H1b (lower sens)", color="#D44B00", alpha = 0.5)
ax1.plot(t, (var[:, 7]), label="H2b (higher sens)", color="#0F57A4", alpha = 0.5)
ax1.set_title("$d_{Hmax} = $" + str(d_Hmax1) + ", $k_1 < k_2$, $H_2$ invader")
ax1.set_yscale("log")
ax1.set_ylim(10**-7,10**1)

k_1 = 5
k_2 = 0
d_Hmax1 = 10**-2
d_Hmax2 = 10**-2
var = []
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))
ax2.plot(t, (var[:, 4]),label="H1a (lower sens)", color="#FF7F0E")
ax2.plot(t, (var[:, 6]), label="H2a (higher sens)", color="#1F77B4")
ax2.plot(t, (var[:, 5]),label="H1b (lower sens)", color="#D44B00", alpha = 0.5)
ax2.plot(t, (var[:, 7]), label="H2b (higher sens)", color="#0F57A4", alpha = 0.5)
ax2.set_title("$d_{Hmax} = $" + str(d_Hmax1) + ", $k_1 > k_2$, $H_2$ invader")
ax2.set_yscale("log")
ax2.set_ylim(10**-7,10**1)

k_1 = 0
k_2 = 5
d_Hmax1 = 10**-3
d_Hmax2 = 10**-3
var = []
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))
ax3.plot(t, (var[:, 4]),label="H1a (lower sens)", color="#FF7F0E")
ax3.plot(t, (var[:, 6]), label="H2a (higher sens)", color="#1F77B4")
ax3.plot(t, (var[:, 5]),label="H1b (lower sens)", color="#D44B00", alpha = 0.5)
ax3.plot(t, (var[:, 7]), label="H2b (higher sens)", color="#0F57A4", alpha = 0.5)
ax3.set_title("$d_{Hmax} = $" + str(d_Hmax1) + ", $k_1 < k_2$, $H_2$ invader")
ax3.set_yscale("log")
ax3.set_ylim(10**-7,10**1)

k_1 = 5
k_2 = 0
d_Hmax1 = 10**-3
d_Hmax2 = 10**-3
var = []
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))
ax4.plot(t, (var[:, 4]),label="H1", color="#FF7F0E")
ax4.plot(t, (var[:, 6]), label="H2", color="#1F77B4")
ax4.plot(t, (var[:, 5]),label="H1b", color="#D44B00", alpha = 0.5)
ax4.plot(t, (var[:, 7]), label="H2b", color="#0F57A4", alpha = 0.5)
ax4.set_title("$d_{Hmax} = $" + str(d_Hmax1) + ", $k_1 > k_2$, $H_2$ invader")
ax4.set_yscale("log")
ax4.set_ylim(10**-7,10**1)

plt.legend(["H1", "H2"])
plt.tight_layout(pad=2.0)

plt.figtext(0.3, -0.1, "$k_1 < k_2$", ha="center", fontsize=20)
plt.figtext(0.78, -0.1, "$k_1 > k_2$", ha="center", fontsize=20)
plt.figtext(-0.1, 0.65, "$d_{Hmax} = 10^-2$", ha="center", fontsize=20, rotation=90)
plt.figtext(-0.1, 0.15, "$d_{Hmax} = 10^-3$", ha="center", fontsize=20, rotation=90)

fig.text(0, 0.5, 'Heterotroph density', va='center', rotation='vertical', fontsize=14)
fig.text(0.5, 0, 'Time', va='center', fontsize=14)

plt.savefig('./output/invasion_timeseries.png', bbox_inches='tight')