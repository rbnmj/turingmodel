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

# adaptability
c_1 = 2 # dispersal adaptability of competitor 1 
c_2 = 2 # dispersal adaptability of competitor 2 
        # 0 = random dispersal, 2 = adaptive dispersal

# dispersal speed 
d_Hmax1 = 0.1 # maximal dispersal rates of competitor 1  
d_Hmax2 = 0.1 # maximal dispersal rates of competitor 2  

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
    d_H1a = var[8]
    d_H2a = var[9]
    d_H1b = var[10]
    d_H2b = var[11]

    # growth rate of autotrophs
    r_a = (r_max * N_a) / (N_h + N_a)
    r_b = (r_max * N_b) / (N_h + N_b)

    # growth rate of competitors
    g_1a = (a_1 * A_a) / (1 + a_1 * h * A_a)
    g_1b = (a_1 * A_b) / (1 + a_1 * h * A_b)
    g_2a = (a_2 * A_a) / (1 + a_2 * h * A_a)    
    g_2b = (a_2 * A_b) / (1 + a_2 * h * A_b)

    # # inflection points
    H_01 = 0.16
    H_02 = 0.16
    
    # dispersal rates of competitors
    d_H1a = d_Hmax1 * ( 1 / (1 + np.exp(c_1 * (H_01 - (H_1a+H_2a)))))
    d_H1b = d_Hmax1 * ( 1 / (1 + np.exp(c_1 * (H_01 - (H_1b+H_2b)))))
    d_H2a = d_Hmax2 * ( 1 / (1 + np.exp(c_2 * (H_02 - (H_1a+H_2a)))))
    d_H2b = d_Hmax2 * ( 1 / (1 + np.exp(c_2 * (H_02 - (H_1b+H_2b)))))
    
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

    return(dN_a, dN_b, dA_a, dA_b, dH_1a, dH_1b, dH_2a, dH_2b, d_H1a, d_H2a, d_H1b, d_H2b)

def find_maxima(x,n):
    """ returns an array with n extreme values of x"""
    
    max_index = signal.argrelmax(x)[0]         # create array with indices of local maxima of x
    
    extrema = x[max_index]                     # array with the actual values of the extrema
       
    if len(extrema) == 0:                      # if all values in x are the same and no extremum is found:
        extrema = np.append(extrema,x[-1])     #   return last value of x in this case
    while len(extrema) < n:                    # if less than n extrema have been found:
        extrema = np.append(extrema,extrema[0])#   repeat last extremum until array has n elements
    while len(extrema) > n:                    # if more than n extrema have been found:
        extrema = np.delete(extrema,-1)        #   delete elements until arrays has n elements
        
    return extrema

t_end = 2000
number_steps = 2000
t = np.linspace(0, t_end, number_steps)

# var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
var0 = [2, 2.5, 2.5, 2, 0.2, 0.3, 0, 0, 0, 0, 0, 0]

num_extr = 12 # set number of maxima to be found

# d_hmax = 10**-2
# dispersal adaptability
d_Hmax1, d_Hmax2 = 10**-2, 10**-2
c_range = np.geomspace(10**-2, 10**2, 100)


Hdiff_extr = []
Hdiff_slope = np.zeros((len(c_range), len(c_range)))
var = []

i = 0
j = 0

for c_2 in tqdm(c_range):
    j = 0
    for c_1 in c_range:
        t_end = 1000
        number_steps = 1000
        t0 = np.linspace(0, t_end, number_steps)
        var0 = [2, 2.5, 2.5, 2, 0.2, 0.3, 0, 0, 0, 0, 0, 0]
        var = integ.odeint(slow, var0, t0)
        #var[var < 1e-8] = 1.1*1e-8

        t_end = 2500
        number_steps = 2500
        t = np.linspace(0, t_end, number_steps)
        var00 = [var[-1,0], var[-1,1], var[-1,2], var[-1,3], 0.5*var[-1,4], 0.5*var[-1,5], 0.5*var[-1,4], 0.5*var[-1,5], 0, 0, 0, 0]
        var = integ.odeint(slow, var00, t)
        
        Hdiff_extr.append(find_maxima(var[200:1000, 6]-var[200:1000, 4],num_extr))
        Hdiff_slope[i, j] = linregress(np.linspace(0, 12, num_extr),Hdiff_extr[0][0:num_extr])[0]

        # workaround to empty lists
        H2_extr = []
        Hdiff_extr = []

        j += 1
    i += 1

np.save('./data/fig9d/Hdiff_slope_10-2.npy', Hdiff_slope)


# d_hmax = 10**0
d_Hmax1, d_Hmax2 = 10**0, 10**0
c_range = np.geomspace(10**-2, 10**2, 100)


Hdiff_extr = []
Hdiff_slope = np.zeros((len(c_range), len(c_range)))
var = []

i = 0
j = 0

for c_2 in tqdm(c_range):
    j = 0
    for c_1 in c_range:
        t_end = 1000
        number_steps = 1000
        t0 = np.linspace(0, t_end, number_steps)
        var0 = [2, 2.5, 2.5, 2, 0.2, 0.3, 0, 0, 0, 0, 0, 0]
        var = integ.odeint(slow, var0, t0)
        #var[var < 1e-8] = 1.1*1e-8

        t_end = 2500
        number_steps = 2500
        t = np.linspace(0, t_end, number_steps)
        var00 = [var[-1,0], var[-1,1], var[-1,2], var[-1,3], 0.5*var[-1,4], 0.5*var[-1,5], 0.5*var[-1,4], 0.5*var[-1,5], 0, 0, 0, 0]
        var = integ.odeint(slow, var00, t)
        
        Hdiff_extr.append(find_maxima(var[200:1000, 6]-var[200:1000, 4],num_extr))
        Hdiff_slope[i, j] = linregress(np.linspace(0, 800, 800),var[0:800,6])[0]

        # workaround to empty lists
        H2_extr = []
        Hdiff_extr = []

        j += 1
    i += 1

np.save('./data/fig9d/Hdiff_slope_10-0.npy', Hdiff_slope)