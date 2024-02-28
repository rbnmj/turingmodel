import numpy as np
from matplotlib import pyplot as plt

# resource dependent dispersal

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
plt.xscale('log') 
plt.xlabel('autotroph density', fontsize=14)
plt.ylabel('dispersal rate of the heterotroph', fontsize=14)
plt.tick_params(axis='both', labelsize=12)
plt.legend()
plt.savefig('./figures/fig4af.png', dpi=300)


# crowding dependent dispersal

d_Hmax1 = 1
H_x_range = np.linspace(0, 10, 1000)
H_0 = 0.16
def dispersalrate(H_x):
    d_H1x = d_Hmax1 * ( 1 / (1 + np.exp(k * (H_0 - H_x))))
    return (H_x, d_H1x)
fig, ax = plt.subplots(figsize=(6, 6))

k = 10
res10 = np.array([dispersalrate(a) for a in H_x_range])
plt.plot(res10[:,0],res10[:,1], label="$k = $" + str(k))
k = 1
res1 = np.array([dispersalrate(a) for a in H_x_range])
plt.plot(res1[:,0],res1[:,1], label="$k = $" + str(k))
k = 0.1
res01 = np.array([dispersalrate(a) for a in H_x_range])
plt.plot(res01[:,0],res01[:,1], label="$k = $" + str(k))
k = 0.01
res001 = np.array([dispersalrate(a) for a in H_x_range])
plt.plot(res001[:,0],res001[:,1], label="$k = $" + str(k))
k = 0
res0 = np.array([dispersalrate(a) for a in H_x_range])
plt.plot(res0[:,0],res0[:,1], label="$k = $" + str(k))
plt.axvline(x=H_0, color='black', linestyle='--', label="$H^*$")
plt.xscale('log') 
plt.xlabel('heterotroph density', fontsize=20)
plt.ylabel('dispersal rate of the heterotroph', fontsize=20)
plt.tick_params(axis='both', labelsize=16)
plt.legend(fontsize=17)
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.savefig('./figures/fig4bf.png', dpi=300)


# growth rate dependent dispersal

d_Hmax1 = 1
A_a_range = np.linspace(0, 10, 100)
def dispersalrate(A_x):
    Gx = 0.33*1*A_x/(1+1*0.53*A_x) - 0.3
    d_H1x = d_Hmax1 / (1+np.exp(k*Gx))
    gx = 1 * A_x / (1 + 1 * 0.53 * A_x)
    return (gx, d_H1x)
fig, ax = plt.subplots(figsize=(6, 6))

k = 100
res100 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res100[:,0],res100[:,1], label="$k = $" + str(k))
k = 10
res10 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res10[:,0],res10[:,1], label="$k = $" + str(k))
k = 1
res1 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res1[:,0],res1[:,1], label="$k = $" + str(k))
k = 0.1
res01 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res01[:,0],res01[:,1], label="$k = $" + str(k))
k = 0
res0 = np.array([dispersalrate(a) for a in A_a_range])
plt.plot(res0[:,0],res0[:,1], label="$k = $" + str(k))
resGx0 = dispersalrate((100/57))
plt.axvline(x=resGx0[0], color='black', linestyle='--', label="$G_{x0}$")
plt.xscale('log') 
plt.xlabel('net growth rate of the heterotroph', fontsize=20)
plt.ylabel('dispersal rate of the heterotroph', fontsize=20)
plt.tick_params(axis='both', labelsize=16)
plt.legend(fontsize=20)
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.savefig('./figures/fig4cf.png', dpi=300)
plt.show()

