import numpy as np
from scipy import integrate as integ
import sys
sys.path.append('./')
from turing_model import TuringModel as tm
from tqdm import tqdm

# time parameters
t_end = 20000
number_steps = 20000
t = np.linspace(0, t_end, number_steps)

# dispersal adaptability
k_1 = 0
k_2 = 0

# maximum dispersal rate
d_Hmax1 = 0
d_Hmax2 = 0
d_Hmax1_range = np.logspace(-4, 1, 100)
d_Hmax2_range = d_Hmax1_range

# initial conditions
var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 0.08, 0.4, 0, 0, 0, 0, 0, 0]
var = []

# result arrays
meandensity_H1x = np.zeros(((len(d_Hmax2_range)),(len(d_Hmax2_range))))
meandensity_H1y = np.zeros(((len(d_Hmax2_range)),(len(d_Hmax2_range))))
meandensity_H2x = np.zeros(((len(d_Hmax2_range)),(len(d_Hmax2_range))))
meandensity_H2y = np.zeros(((len(d_Hmax2_range)),(len(d_Hmax2_range))))
var = []

i = 0
j = 0

for d_Hmax2 in tqdm(d_Hmax2_range):
    j = 0
    for d_Hmax1 in d_Hmax1_range:
        model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
        var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))

        meandensity_H1x[i, j] = np.mean(var[-200:-1, 4])
        meandensity_H1y[i, j] = np.mean(var[-200:-1, 5])
        meandensity_H2x[i, j] = np.mean(var[-200:-1, 6])
        meandensity_H2y[i, j] = np.mean(var[-200:-1, 7])

        j += 1
    i += 1

np.savetxt('./data/fig5d/meandensity_H1x.csv', meandensity_H1x, delimiter=",")
np.savetxt('./data/fig5d/meandensity_H1y.csv', meandensity_H1y, delimiter=",")
np.savetxt('./data/fig5d/meandensity_H2x.csv', meandensity_H2x, delimiter=",")
np.savetxt('./data/fig5d/meandensity_H2y.csv', meandensity_H2y, delimiter=",")