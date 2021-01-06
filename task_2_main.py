#-----------------------------------------------------------------------------
#PHY3054
#Assignment 1
#Student: 6463360
#Task 2
#---Programme Description-----------------------------------------------------
#This programme calculates the enclosed mass of an orbit around Andromeda and
#the density, assuming the matter is uniformly spread in a spherical region
#within the orbit.

#This is then compared to a calculation for the critical density of the
#universe.
#-----------------------------------------------------------------------------


#---Import Useful Libraries---
import numpy as np


#--Calculating the average density of Andromeda-------------------------------
#---Set Variables and constants---
R = 20 * 1000 * 3.086e16 #Radius of orbit in units of m.
V = 226 * 1000 #Tangental velocity in units of m/s.
G = 6.67430e-11 #Gravitational constant in units of m^3/(kg.s^2).


#---Make function to preform calculation---
#Calculates enclosed mass of the orbit taking radius and velocity of orbital.
#This function returns the mass in units of grams.
def enclosed_mass(X, Y):
    M = Y**2 * X / G
    return M * 1000 #grams

print("") #Adds some space to the terminal output for neatness.


#---Caculate enclosed mass of Andromeda---
print("Enclosed Mass of Andromeda =", '%.3e' %enclosed_mass(R, V), "kg")


#---Calculate average density---
#Assume the galaxy is a sphere so the volume is 4/3*Pi*r^3
R_cm = R * 100 #cm
vol = 4 / 3 * np.pi * R_cm**3

rho = enclosed_mass(R, V) / vol
print("Density of Andromeda =", '%.3e' %rho, "g/cm\u00b3")


#---Calculating Critical Density of the Universe------------------------------
#---Set vairables---
Ho = 70 #km/sMpc


#---Do calculation---
crit_rho = (3 * Ho**2) / (8 * np.pi * G) * 1000 * (3.086e24)**2 #g/cm^3
print("Critical density of the Universe =", '%.3e' %crit_rho, "g/cm\u00b3")


#---Calculate the density ration between--------------------------------------
print("The density ratio, Andromeda:Universe =", \
      '%.3e' %(rho / crit_rho))

print("") #Adds some space to the terminal output for neatness.
