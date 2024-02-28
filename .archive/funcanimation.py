import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy import integrate as integ

from turing_model import TuringModel as tm

t_end = 2000
number_steps = 2000
t = np.linspace(0, t_end, number_steps)


#var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 0.08, 0.4, 0, 0, 0, 0, 0, 0]

var = []
k_1 = 5
k_2 = 0
d_Hmax1 = 0.001
d_Hmax2 = 0.001
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()
dimension = (5, 5)
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy import integrate as integ

from turing_model import TuringModel as tm

t_end = 2000
number_steps = 2000
t = np.linspace(0, t_end, number_steps)


#var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 0.08, 0.4, 0, 0, 0, 0, 0, 0]

var = []
k_1 = 5
k_2 = 0
d_Hmax1 = 0.001
d_Hmax2 = 0.001
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()
data = var[:, 4]
sns.heatmap((data,data))
plt.show()
# def init():
#     sns.heatmap(np.zeros(dimension), cbar=False)

# def animate(i):
#     data = np.random.rand(dimension[0], dimension[1])
#     sns.heatmap(data, cbar=False)

# anim = animation.FuncAnimation(fig, animate, init_func=init, frames=20, repeat=False)

# plt.show()