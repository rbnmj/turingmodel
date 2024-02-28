import numpy as np
from scipy import integrate as integ
from scipy import signal as signal
from scipy.stats import linregress
from tqdm import tqdm

# set parameters
S = 4.8 # Nutrient supply concentration
D = 0.3 # Dilution rate
N_h = 1.5 # half saturation constant for nutrient uptake
r_max = 0.7 # growth rate of autotroph
h = 0.53 # handling time
e = 0.33 # conversion efficiency of competitor
d_N = 1 # Dispersal rate of nutrients 
d_A = 0.001 # dispersal rate of autotrophs

# competitiveness 
a_1 = 1 # attack rate of competitor 1 
a_2 = 1 # attack rate of competitor 2 

def slow(var, t):
    # fill var
    N_a = var[0]
    N_b = var[1]
    A_a = var[2]
    A_b = var[3]
    H_1a = var[4]
    H_1b = var[5]
    H_2a = var[6]
    H_2b = var[7]
    g_1a = var[8]
    g_1b = var[9]
    g_2a = var[10]
    g_2b = var[11]

    # growth rate of autotrophs
    r_a = (r_max * N_a) / (N_h + N_a)
    r_b = (r_max * N_b) / (N_h + N_b)

    # growth rate of competitors
    g_1a = (a_1 * A_a) / (1 + a_1 * h * A_a)
    g_1b = (a_1 * A_b) / (1 + a_1 * h * A_b)
    g_2a = (a_2 * A_a) / (1 + a_2 * h * A_a)
    g_2b = (a_2 * A_b) / (1 + a_2 * h * A_b)

    # inflection points
    Gx = e * a_1 * A_a/(1+a_1 * h * A_a) - D
    Gy = e * a_1 * A_b/(1+a_1 * h * A_b) - D
    
    # dispersal rates of competitors
    d_H1a = d_Hmax1 / (1 + np.exp(k_1 * Gx))
    d_H1b = d_Hmax1 / (1 + np.exp(k_1 * Gy))
    d_H2a = d_Hmax2 / (1 + np.exp(k_2 * Gx))
    d_H2b = d_Hmax2 / (1 + np.exp(k_2 * Gy))

    # change of nutrients
    dN_a = D * (S - N_a) - r_a * A_a + d_N * (N_b - N_a)
    dN_b = D * (S - N_b) - r_b * A_b + d_N * (N_a - N_b)

    # change of autotrophs
    dA_a = r_a * A_a - ((g_1a * H_1a) + (g_2a * H_2a)) - D * A_a + d_A * (A_b - A_a)
    dA_b = r_b * A_b - ((g_1b * H_1b) + (g_2b * H_2b)) - D * A_b + d_A * (A_a - A_b)

    # change of competitors
    dH_1a = e * g_1a * H_1a - D * H_1a - d_H1a * H_1a + d_H1b * H_1b
    dH_1b = e * g_1b * H_1b - D * H_1b - d_H1b * H_1b + d_H1a * H_1a
    dH_2a = e * g_2a * H_2a - D * H_2a - d_H2a * H_2a + d_H2b * H_2b
    dH_2b = e * g_2b * H_2b - D * H_2b - d_H2b * H_2b + d_H2a * H_2a

    return(dN_a, dN_b, dA_a, dA_b, dH_1a, dH_1b, dH_2a, dH_2b, g_1a, g_1b, g_2a, g_2b)

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

t_end = 3000
number_steps = 3000
t1 = np.linspace(0, t_end, number_steps)

# dispersal adaptability
k_1_range = np.geomspace(10**-1, 10**2, 100)
k_2_range = np.geomspace(10**-1, 10**2, 100)

# maximum dispersal rate
d_Hmax1 = 10**-3
d_Hmax2 = 10**-3

var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 0, 0, 0, 0, 0, 0]


num_extr = 60 # set number of maxima to be found #40

H2_extr = []
slopeH2 = np.zeros((len(k_1_range), len(k_2_range)))
var = []

i = 0
j = 0

for k_2 in tqdm(k_2_range):
    j = 0
    for k_1 in k_1_range:
        var = integ.odeint(slow, var0, t1)

        t_end = 10000
        number_steps = 10000
        t = np.linspace(0, t_end, number_steps)
        var00 = [var[-1,0], var[-1,1], var[-1,2], var[-1,3], var[-1,4], var[-1,5], 10**-6, 10**-6, 0, 0, 0, 0]
        var = integ.odeint(slow, var00, t)
    
        var = np.where(var < 10**-6, 10**-6, var)

        H2_extr.append(find_maxima(np.log(var[:, 6])+np.log(var[:, 6]),num_extr))

        # results[i,j] = ...
        slopeH2[i, j] = linregress(np.linspace(1, 20, 40),H2_extr[0][20:num_extr])[0]

        # workaround to empty lists
        H2_extr = []

        j += 1
    i += 1
np.load('./data/fig10d/slopeH2.npy', slopeH2)