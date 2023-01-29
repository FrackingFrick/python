#Solve equation x_n+1=r*x_n *(1−{x_n})
from matplotlib import pyplot as plt 
#values
z_0=0.5
r=2.9

n_max=50

z=z_0

z_arr=[z_0]

for n in range(n_max):
    z_new=r*z*(1-z)
    z=z_new
    z_arr.append(z)

#create figure
fig, ax= plt.subplots()

#plot data
ax.scatter(range(n_max+1),z_arr)
ax.set_xlabel("n")
ax.set_ylabel("z_n")
ax.set_title("x_n+1=r*x_n *(1−x_n)")
ax.grid(True)

plt.show()