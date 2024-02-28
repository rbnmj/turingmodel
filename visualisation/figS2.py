import numpy as np
from matplotlib import pyplot as plt
from scipy import integrate as integ
from matplotlib.lines import Line2D
import sys
sys.path.append('./')
from turing_model import TuringModel as tm

t_end = 2000
number_steps = 2000
t1 = np.linspace(0, t_end, number_steps)
var0 = [2, 2.5, 2.5, 2, 0.8, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
start = 22000#24900#24920
end = 22200#25050#24985
var = []
k_1 = 0.44
k_2 = 0.4
d_Hmax1 = 10**-3
d_Hmax2 = 10**-3
model = tm(var0, t1, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t1, args=(model,))
t_end = 25050
number_steps = 25050
t = np.linspace(0, t_end, number_steps)
var00 = [var[-1,0], var[-1,1], var[-1,2], var[-1,3], 0.5*var[-1,4], 0.5*var[-1,5], 0.5*var[-1,4], 0.5*var[-1,5], 0, 0, 0, 0, 0, 0, 0, 0]
model = tm(var00, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var00, t, args=(model,))

## flow calcs
# inflection points
x_01 = 0.3 / (1 * (0.33 - 0.53 * 0.3))
x_02 = 0.3 / (1 * (0.33 - 0.53 * 0.3))
flowA_x = var[start:end, 2]
flowA_y = var[start:end, 3]
# dispersal rates of competitors
f_d_H1a = d_Hmax1 / (1 + np.exp(k_1 * (flowA_x - x_01)))
f_d_H1b = d_Hmax1 / (1 + np.exp(k_1 * (flowA_y - x_01)))
f_d_H2a = d_Hmax2 / (1 + np.exp(k_2 * (flowA_x - x_02)))
f_d_H2b = d_Hmax2 / (1 + np.exp(k_2 * (flowA_y - x_02)))
# flow rates
flow1xy = (f_d_H1a) / (f_d_H1a + f_d_H1b)
flow1yx = (f_d_H1b) / (f_d_H1a + f_d_H1b)
flow2xy = (f_d_H2a) / (f_d_H2a + f_d_H2b)
flow2yx = (f_d_H2b) / (f_d_H2a + f_d_H2b)

a_x = var[start:end, 2]

plt.axhline(1, color="grey", linestyle="--", alpha=0.5)
plt.axhline(0, color="grey", linestyle="--", alpha=0.5)
plt.plot(a_x, flow1xy, color="tab:orange", label="H1 low $k$")
plt.plot(a_x, flow2xy, color="tab:blue", label="H2 low $k$")
plt.xlabel("Autotroph density", fontsize=17)
plt.ylabel("Proportion of dispersal on patch x", fontsize=17)
plt.ylim(-0.03,1.03)
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)

legend_elements = [
    Line2D([0], [0], linestyle='-', color='black', label='low sensitivity'),
    # Line2D([0], [0], linestyle='--', color='black', label='intermediate sensitivity'),
    # Line2D([0], [0], linestyle=':', color='black', label='high sensitivity'),
    Line2D([0], [0], linestyle='-', color='tab:orange', label='$H_1$'),
    Line2D([0], [0], linestyle='-', color='tab:blue', label='$H_2$')
]
plt.tight_layout()
plt.legend(handles=legend_elements, fontsize =16)
plt.savefig('./figures/figS2f.png', dpi=300)
plt.show()
