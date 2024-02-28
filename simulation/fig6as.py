import numpy as np
from scipy import integrate as integ
from matplotlib import pyplot as plt
from tqdm import tqdm
import sys
sys.path.append('./')
from turing_model import TuringModel as tm


d_Hmax1_range = np.linspace(4*10**0, 6*10**0, 25)

var = []
xlen = np.linspace(0, 500, 500)
H1x = np.zeros((len(xlen),len(d_Hmax1_range)))
H1y = np.zeros((len(xlen),len(d_Hmax1_range)))

k_1 = 0
k_2 = 0
d_Hmax1 = 10**1
d_Hmax2 = 10**-3

start = 19500
end = 20000

i = 0

for d_Hmax1 in tqdm(d_Hmax1_range):
    t_end = 3000
    number_steps = 3000
    t1 = np.linspace(0, t_end, number_steps)
    var0 = [2, 2.5, 2.5, 2, 0.8, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    var = []
    model = tm(var0, t1, k_1, k_2, d_Hmax1, d_Hmax2)
    var = integ.odeint(tm.equations_wrapper, var0, t1, args=(model,))
    t_end = 20000
    number_steps = 20000
    t = np.linspace(0, t_end, number_steps)
    var00 = [var[-1,0], var[-1,1], var[-1,2], var[-1,3], 0.5*var[-1,4], 0.5*var[-1,5], 0.5*var[-1,4], 0.5*var[-1,5], 0, 0, 0, 0, 0, 0, 0, 0]
    model = tm(var00, t, k_1, k_2, d_Hmax1, d_Hmax2)
    var = integ.odeint(tm.equations_wrapper, var00, t, args=(model,))

    H1x[:,i] = var[start:end,4]
    H1y[:,i] = var[start:end,5]

    i += 1
np.save('./data/fig6ad/H1x.npy', H1x)
np.save('./data/fig6ad/H1y.npy', H1y)