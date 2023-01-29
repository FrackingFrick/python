#Solve equations of motion for a mass hanging from a string
import matplotlib.pyplot as plt
#Define constants
g= 10
k=1
m=1
l=0
b=0.25

#Initial values
x_0=1
v_0=0

#time variables
t_0=0
t_max=20
dt=0.1 #timestep

#Init
x=x_0
v=v_0
t=t_0

#Arr to store
x_arr=[x_0]
v_arr=[v_0]
t_arr=[t_0]

#Time loop
while t<t_max:
    x_new = x + dt * v
    v_new = v + dt * (g - k/m * (x - l) - b/m *v)
    t_new = t + dt

    x=x_new
    v=v_new
    t=t_new

    x_arr.append(x)
    v_arr.append(v)
    t_arr.append(t)

#Plot data
fig,ax=plt.subplots()
ax.scatter(t_arr,x_arr)
plt.show()