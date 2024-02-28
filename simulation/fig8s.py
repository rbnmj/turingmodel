import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as integ
from scipy.stats import linregress
from tqdm import tqdm
import sys
sys.path.append('./')
from turing_model import TuringModel as tm
from scipy import signal

def find_maxima(x,n):
    """ returns an array with n extreme values of x"""
    
    max_index = signal.argrelmax(x)[0]         # create array with indices of local maxima of x
    
    #ext_index = np.append(max_index)           # array with indices of local extrema in x
    #ext_index = np.sort(ext_index)             # sort array (alternating minima and maxima)
    extrema = x[max_index]                     # array with the actual values of the extrema
       
    if len(extrema) == 0:                      # if all values in x are the same and no extremum is found:
        extrema = np.append(extrema,x[-1])     #   return last value of x in this case
    while len(extrema) < n:                    # if less than n extrema have been found:
        extrema = np.append(extrema,extrema[0])#   repeat last extremum until array has n elements
    while len(extrema) > n:                    # if more than n extrema have been found:
        extrema = np.delete(extrema,-1)        #   delete elements until arrays has n elements
        
    return extrema

num_extr = 40 # set number of maxima to be found
t_end = 500
number_steps = 500
t = np.linspace(0, t_end, number_steps)
k_1 = 0.01
k_2 = 0.01
k_1_range = np.geomspace(10**-2, 10**0, 100)
k_2_range = np.geomspace(10**-2, 10**0, 100)
#var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

d_Hmax1 = 10**0
d_Hmax2 = d_Hmax1

slopeH2 = np.zeros((len(k_1_range), len(k_2_range)))
H2_extr = []
var = []

i = 0
j = 0
for k_2 in tqdm(k_2_range):
    j = 0
    for k_1 in k_1_range:
        model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
        var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))
        var[var < 1e-8] = 1*1e-8

        var00 = [var[-1,0], var[-1,1], var[-1,2], var[-1,3], var[-1,4], var[-1,5], 10**-6, 10**-6, 0, 0, 0, 0, 0, 0, 0, 0]
        model = tm(var00, t, k_1, k_2, d_Hmax1, d_Hmax2)
        var = integ.odeint(tm.equations_wrapper, var00, t, args=(model,))
        var[var < 1e-8] = 1.1*1e-8

        slopeH2[i,j] = linregress(np.linspace(1, 20, 300),np.log(var[100:400,6]))[0]

        j += 1
    i += 1
np.savetxt("./data/fig8d/H2Slope.csv", slopeH2, delimiter=",")