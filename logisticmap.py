#Solve equation x_n+1=r*x_n *(1−{x_n})
from matplotlib import pyplot as plt 
import numpy as np 

# initialize an array of 0s and specify starting values and r constant
steps = 50
x = np.zeros(steps + 1)
y = np.zeros(steps + 1)
x[0], y[0] = 0, 0.4

r = 2.9

# loop over the steps and replace array values with calculations
for i in range(steps):
	y[i+1] = r * y[i] * (1 - y[i])
	x[i+1] = x[i] + 1

# plot the figure!
fig, ax = plt.subplots()
ax.plot(x, y, alpha=0.5)
ax.set(xlabel='Time (years)', ylabel='Population (fraction of max)')
plt.show()

