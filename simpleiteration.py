#Solve the equation z_{n+1}= z_n^2 +1, z_0=0
import matplotlib.pyplot as plt 
#Define initial value
z_0=0

#Max value
n_max=10

#Init z
z=z_0

#Arr for storing
z_array=[z_0]
#Loop to make the calculation
for n in range(n_max):
    z_new=z**2 +1
    z=z_new
    z_array.append(z)

#create figure
fig, ax= plt.subplots()

#plot data
ax.scatter(range(n_max+1),z_array)
ax.set_xlabel("n")
ax.set_ylabel("z_n")
ax.set_title("z_{n+1}= z_n^2 +1, z_0=0")
ax.grid(True)

#display
plt.show()