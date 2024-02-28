import numpy as np
from scipy import integrate as integ
import sys
sys.path.append('./')
from turing_model import TuringModel as tm

t_end = 600
number_steps = 600
t = np.linspace(0, t_end, number_steps)
k_1 = 0
k_2 = 0
var0 = [2, 2.5, 2.5, 2, 0.008, 0.04, 0.008, 0.04, 0, 0, 0, 0, 0, 0,0,0]
#var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]

# oscillatory pattern formation
var = []
d_Hmax1 = 10**-2
d_Hmax2 = 10**-3
H1osc = np.zeros(((len(t)), 2))
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))
H1osc[:,0] = var[:,4]
H1osc[:,1] = var[:,5]

# static pattern formation
var = []
d_Hmax1 = 10**0
d_Hmax2 = 10**2
H1static = np.zeros(((len(t)), 2))
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))
H1static[:,0] = var[:,4]
H1static[:,1] = var[:,5]

# saving 
np.save('./data/fig1d/H1osc.npy', H1osc)
np.save('./data/fig1d/H1static.npy', H1static)