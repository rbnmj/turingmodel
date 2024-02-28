import numpy as np
from scipy import integrate as integ
from matplotlib import pyplot as plt
from scipy import signal as signal

# parameters
S = 4.8  # Nutrient supply concentration
D = 0.3  # Dilution rate
N_h = 1.5  # half saturation constant for nutrient uptake
r_max = 0.7  # growth rate of autotroph
h = 0.53  # handling time
e = 0.33  # conversion efficiency of competitor
d_N = 1  # Dispersal rate of nutrients
d_A = 0.001  # dispersal rate of autotrophs
a_1 = 1  # attack rate of competitor 1
a_2 = 1  # attack rate of competitor 2
k_1 = 10**-1  # dispersal adaptability for competitor 1
k_2 = 10**1  # dispersal adaptability for competitor 2
d_Hmax1 = 10**-3  # maximum dispersal rate of competitor 1
d_Hmax2 = 10**-3  # maximum dispersal rate of competitor 2


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
    g_1a = var[12]
    g_1b = var[13]
    g_2a = var[14]
    g_2b = var[15]

    # growth rate of autotrophs
    r_a = (r_max * N_a) / (N_h + N_a)
    r_b = (r_max * N_b) / (N_h + N_b)

    # growth rate of competitors
    g_1a = (a_1 * A_a) / (1 + a_1 * h * A_a)
    g_1b = (a_1 * A_b) / (1 + a_1 * h * A_b)
    g_2a = (a_2 * A_a) / (1 + a_2 * h * A_a)
    g_2b = (a_2 * A_b) / (1 + a_2 * h * A_b)

    # inflection points
    x_01 = D / (a_1 * (e - h * D))
    x_02 = D / (a_2 * (e - h * D))
    
    # dispersal rates of competitors
    d_H1a = d_Hmax1 / (1 + np.exp(k_1 * (A_a - x_01)))
    d_H1b = d_Hmax1 / (1 + np.exp(k_1 * (A_b - x_01)))
    d_H2a = d_Hmax2 / (1 + np.exp(k_2 * (A_a - x_02)))
    d_H2b = d_Hmax2 / (1 + np.exp(k_2 * (A_b - x_02)))

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

    H1_loss = d_H1a-(d_H1a * dH_1a)/(1 + np.exp(k_1 * (A_a - x_01)))
    H2_loss = d_H2a-(d_H2a * dH_2a)/(1 + np.exp(k_2 * (A_a - x_02)))

    return (dN_a, dN_b, dA_a, dA_b, dH_1a, dH_1b, dH_2a, dH_2b, d_H1a, d_H2a, d_H1b, d_H2b, g_1a, g_1b, g_2a, g_2b)


## simulation 

# "prep" simulation
# simulating H1 to fixpoint
t_end = 5000
number_steps = 5000
t1 = np.linspace(0, t_end, number_steps)
var0 = [2, 2.5, 2.5, 2, 0.8, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
var = []
var = integ.odeint(slow, var0, t1)

# "actual" simulation
# adding H2 
t_end = 25000
number_steps = 25000
t = np.linspace(0, t_end, number_steps)
var00 = [var[-1,0], var[-1,1], var[-1,2], var[-1,3], 0.5*var[-1,4], 0.5*var[-1,5], 0.5*var[-1,4], 0.5*var[-1,5], 0, 0, 0, 0, 0, 0, 0, 0]
var = integ.odeint(slow, var00, t)

## <- start & end slice the time series for plotting -> ##
## <- adjust start & end if the simulation length (t_end or number_steps) is changed -> ##
start = 24900
end = 25000

## Fitness calculations
# extracting results
F1_H1x = var[start:end, 4]
F1_H1y = var[start:end, 5]
F2_H2x = var[start:end, 6]
F2_H2y = var[start:end, 7]

# calculating growth rates from autotroph densities
Ax = var[start:end, 2]
Ay = var[start:end, 3]
F1_gx = (1 * Ax) / (1 + 1 * 0.53 * Ax)
F1_gy = (1 * Ay) / (1 + 1 * 0.53 * Ay)
F2_gx = (1 * Ax) / (1 + 1 * 0.53 * Ax)
F2_gy = (1 * Ay) / (1 + 1 * 0.53 * Ay)

# calculating fitness
F1 = F1_gx * (F1_H1x/(F1_H1x+F1_H1y)) + F1_gy * (F1_H1y/(F1_H1x+F1_H1y))
F2 = F2_gx * (F2_H2x/(F2_H2x+F2_H2y)) + F2_gy * (F2_H2y/(F2_H2x+F2_H2y))

## plotting
fig, (ax1, ax2)=plt.subplots(2)

# plotting heterotroph densities
ax1.plot(t[start:end], var[start:end, 4], label="$H_{1,x}$",color="tab:orange")
ax1.plot(t[start:end], var[start:end, 5], label="$H_{1,y}$",color="tab:orange", linestyle="--")
ax1.plot(t[start:end], var[start:end, 6], label="$H_{2,x}$",color="tab:blue")
ax1.plot(t[start:end], var[start:end, 7], label="$H_{2,y}$",color="tab:blue", linestyle="--")
ax1.set_title("$k_1 = $ " + str(k_1) + ", $k_2 = $ " + str(k_2) + ", $d_{max, 1} = $ " + str(d_Hmax1)+ ", $d_{max, 2} = $ " + str(d_Hmax2))
ax1.set_ylabel("Heterotroph density")
ax1.legend(loc="lower left")

# plotting autotrophs
ax2.plot(t[start:start+1], var[start:start+1, 2], label="$F_1 - F_2$",color="black")
ax2.plot(t[start:end], var[start:end:, 2], label="$A_x$",color="tab:green")
ax2.plot(t[start:end], var[start:end:, 3], label="$A_y$",color="tab:green", linestyle="--")
ax2.set_xlabel("Time")
ax2.set_ylabel("Autotroph density")
ax2.legend(loc="lower left")

# plotting fitness
ax3 = ax2.twinx()
ax3.plot(t[start:end], F1 - F2, label="F1 - F2", color="black", linewidth=2)
ax3.set_ylabel("F1-F2")
# plotting F1-F2 = 0
ax3.axhline(0, color="black", alpha=0.5, linestyle="--")

plt.tight_layout()
plt.show()