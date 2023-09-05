import numpy as np
from matplotlib import pyplot as plt

d_Hmax1 = 1
A_a_range = np.linspace(0, 10, 100)
x_01 = 0.3 / (1 * (0.33 - 0.53 * 0.3))
def dispersalrate(A_a):
    d_H1a = d_Hmax1 / (1 + np.exp(k * (A_a - x_01)))
    return (A_a, d_H1a)

k = 10
res10 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res10[:,0],res10[:,1], label="$k = $" + str(k))
k = 1
res1 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res1[:,0],res1[:,1], label="$k = $" + str(k))
k = 0.1
res01 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res01[:,0],res01[:,1], label="$k = $" + str(k))
k = 0.01
res001 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res001[:,0],res001[:,1], label="$k = $" + str(k))
k = 0
res0 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res0[:,0],res0[:,1], label="$k = $" + str(k))
plt.axvline(x=x_01, color='black', linestyle='--', label="$x_{01}$")
#plt.yscale('log')
plt.xscale('log') 
# plt.ylim(0,1)
# plt.xlim(10**-1,10**1)
plt.xlabel('Autotroph density')
plt.ylabel('Dispersal rate of the heterotroph')
plt.legend()
plt.savefig('./output/dispersalrate_over_autotrophdensity.png')
plt.show()




