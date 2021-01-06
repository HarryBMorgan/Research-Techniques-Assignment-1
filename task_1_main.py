#-----------------------------------------------------------------------------
#PHY3054
#Assignment 1
#Student: 6463360
#Task 1
#---Programme Description-----------------------------------------------------
#This programme calculates the first 3 spherical Bessel functions and plots
#them to a common graph. The graph is then saves as a PNG.
#The fnctionality at x = 0 has been considered and accounted for.
#-----------------------------------------------------------------------------


#---Import useful libraries---
import numpy as np
import matplotlib.pyplot as plt


#---Define some vairables---
x = np.linspace(0, 20, 1000) #Range of x-values to be used.


#---Create Bessel Caculation Function---
#This function takes the arguments x (an array) and n (defines the order
#of Bessel function desired).
#It is capable of calculating the first, second or third Bessel function.
#For n = 0, x = 0, the bessel returns 1.
#For n > 0, x = 0, the bessel returns 0.
def bessel_n(z, n):
    y = np.empty(len(z))
    for i in range(len(z)):
        if n == 0: #The first Bessel function.
            if z[i] == 0: y[i] = 1 #If z = 0 the value is known to be 1.
            #For all other z-values do the calculation for first Bessel.
            if z[i] > 0: y[i] = np.sin(z[i]) / z[i]
        if n == 1: #The second Bessel function.
            if z[i] == 0: y[i] = 0 #If z = 0 the value is known to be 0.
             #For all other z-values do the calculation for second Bessel.
            if z[i] > 0: y[i] = np.sin(z[i]) / (z[i]**2) - np.cos(z[i]) / z[i]
        if n == 2: #The third Bessel function.
            if z[i] == 0: y[i] = 0 #If z = 0 the value is known to be 0.
            #For all other z-values do the calculation for third Bessel.
            if z[i] > 0: y[i] = (3 / (z[i]**2) - 1) * np.sin(z[i]) / z[i] - \
                                3 * np.cos(z[i]) / (z[i]**2)
    return y


#---Populate arrays for Bessel functions of order 0, 1, and 2---
b0 = bessel_n(x, 0)
b1 = bessel_n(x, 1)
b2 = bessel_n(x, 2)


#---Plot the functions nicely---
plt.plot(x, b0, 'r', linestyle=':', label="$J_0(x)$")
plt.plot(x, b1, 'g', linestyle='--', label="$J_1(x)$")
plt.plot(x, b2, 'b', label="$J_2(x)$")
plt.legend()
plt.title("Spherical Bessel Function, $J_n(x)$", fontweight='bold')
plt.xlim(0, 20)
plt.xlabel("X")
plt.ylim(-0.25, 1)
plt.ylabel("$J_n(x)$")
plt.axhline(y=0, color='black')
#Save the figure as a PNG.
plt.savefig("bessel_function.png")
plt.show()
