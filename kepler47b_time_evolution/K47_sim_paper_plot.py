
# coding: utf-8

# In[2]:

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sympy as sp
from sympy import *

#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (18,15)
mpl.rcParams['font.size'] = 22.0

fig, axes = plt.subplots(ncols=2, nrows=2, sharey=False)
fig.set_size_inches(21,12)

# Each line gets it own color
colores = ["C" + str(n) for n in range(6)]

#Since this data is not generalized nor looped, I will be very specific about the values written on here
observed_k47_semi_major_axis = 0.0836 # In AU
observed_k47_orbital_period = 7.44837695 # In days
observed_k47_ecc = 0.0234
observed_cbp_semi_major_axis = 0.2956 # In AU
observed_cbp_ecc = 0.035

file_name = "kepler47"
star_file = ".secondary.forward"
cbp_file = ".cbp.forward"
#We'll define a function that'll call in all parameters of the secondary star
def cast_simulation_star(file, color):
    binary_data = np.genfromtxt(file) #Chooses the secondary star
    binary_time = binary_data[:,0] #Time axis of each secondary binary file
    binary_eccentricity = binary_data[:,6] #Eccentricity axis of each secondary binary file
    binary_semi_major_axis = binary_data[:,3] #Semi-major axis of secondary star
    binary_semi_major_crit = binary_data[:,10] #Critical semi-major axis of the binary stars
    binary_orbital_period = binary_data[:,7] #Orbital period of the binary stars
    return (binary_time, binary_eccentricity, binary_semi_major_axis, 
            binary_semi_major_crit, binary_orbital_period, colores[color])
def cast_simulation_cbp(file, color):
    cbp_data = np.genfromtxt(file) #Chooses the cbp
    cbp_time = cbp_data[:,0] #Time axis of cbp file
    cbp_eccentricity = cbp_data[:,5] #Eccentricity axis of cbp file
    cbp_semi_major_axis = cbp_data[:,1] #Semi-major axis of cbp
    return (cbp_time, cbp_eccentricity, cbp_semi_major_axis, 
            colores[color])

star = cast_simulation_star(file_name + star_file, 1)
cbp = cast_simulation_cbp(file_name + cbp_file, 0)

accent_color1 = "#388e3c" #green
accent_color2 = "#ffeb3b" #yellow
star_color_sim = accent_color2
star_color_obs = "purple"
planet_color_sim = accent_color1
planet_color_obs = "purple"
acrit_color = colores[0]

#Plotting the simulated and observed semi-major axis of the star on the top-left panel
axes[0,0].plot(star[0], star[2], lw=3, 
               color = star_color_sim, ls = "-", 
               label = "Simulated " + r"$a_{47B}$") #Simulated K47B data
axes[0,0].plot(star[0], [observed_k47_semi_major_axis for i in range(len(star[0]))], 
               lw=3, color = star_color_obs, ls = "--", 
               label = "Observed " + r"$a_{47B}$") #Observed semi-major axis of K47B
axes[0,0].set_xscale("log")
axes[0,0].set_xlabel("Time [yr]")
axes[0,0].set_xlim(xmin=1e+6)
axes[0,0].set_ylabel("Semi-Major axis [AU]")

#Plotting the simulated and observed semi-major axis of the cbp on the top-right panel
axes[0,1].plot(cbp[0], cbp[2], lw=3, 
               color = planet_color_sim, ls = "-", 
               label = "K-47b simulated") #Simulated K47b data
axes[0,1].plot(cbp[0], [observed_cbp_semi_major_axis for i in range(len(cbp[0]))], 
               lw=3, color = planet_color_obs, ls = "--", 
               label = "K-47b observed") #Observed semi-major axis of K47b
axes[0,1].plot(star[0], star[3], lw=3, 
               color = acrit_color, ls = "--", 
               label = "Simulated " + r"$a_{crit}$") #Simulated a_crit
axes[0,1].set_xscale("log")
axes[0,1].set_xlabel("Time [yr]")
axes[0,1].set_xlim(xmin=1e+6)
axes[0,1].set_ylabel("Semi-Major axis [AU]")
axes[0,1].legend(loc = "center right")

#Plotting the simulated and observed binary eccentricity of the star on the bottom-left panel
axes[1,0].plot(star[0], star[1], lw=3, 
               color = star_color_sim, ls = "-", 
               label = "K-47B simulated") #Simulated K47B data
axes[1,0].plot(star[0], [observed_k47_ecc for i in range(len(star[0]))], 
               lw=3, color = star_color_obs, ls = "--", 
               label = "K-47B observed") #Observed binary eccentricity of K47B
axes[1,0].set_xscale("log")
axes[1,0].set_xlabel("Time [yr]")
axes[1,0].set_xlim(xmin=1e+6)
axes[1,0].set_ylabel("Binary Eccentricity")
axes[1,0].legend(loc = "center left")

#Plotting the simulated and observed free eccentricity of the cbp on the bottom-right panel
axes[1,1].plot(cbp[0], cbp[1], lw=3, 
               color = planet_color_sim, ls = "-", 
               label = "Simulated " + r"$e_{free, 47b}$") #Simulated K47b data
axes[1,1].plot(cbp[0], [observed_cbp_ecc for i in range(len(cbp[0]))], 
               lw=3, color = planet_color_obs, ls = "--", 
               label = "Observed " + r"$e_{free, 47b}$") #Observed free eccentricity of K47b
axes[1,1].set_xscale("log")
axes[1,1].set_xlabel("Time [yr]")
axes[1,1].set_xlim(xmin=1e+6)
axes[1,1].set_ylabel("Free Eccentricity")
 
fig.tight_layout()
fig.savefig("kepler47" + ".png", bbox_inches="tight")

