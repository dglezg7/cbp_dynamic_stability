
# coding: utf-8

# In[2]:

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import astropy.units as u
import sympy as sp
from sympy import *

#Typical plot parameters that make for pretty plots
mpl.rcParams['font.size'] = 22.0
fig, axes = plt.subplots(ncols=1, nrows=3, sharey=False)
mpl.rcParams['figure.figsize'] = (36,27)
fig.set_size_inches(21,16)

# Each line gets it own color
colores = ["C" + str(n) for n in range(6)]

file_name = "habitable_cbp" #main name of the simulation
star_file = ".secondary.forward" #Summons secondary star simulation
cbp_file = ".cbp.forward" #Summons cbp simulation

#Defining a function that'll call in all parameters of the secondary star
def cast_simulation_star(file, color):
    binary_data = np.genfromtxt(file) #Chooses the secondary star
    binary_time = binary_data[:,0] #Time axis of each secondary binary file
    binary_eccentricity = binary_data[:,6] #Eccentricity axis of each secondary binary file
    binary_semi_major_axis = binary_data[:,3] #Semi-major axis of secondary star
    binary_semi_major_crit = binary_data[:,10] #Critical semi-major axis of the binary stars
    binary_orbital_period = binary_data[:,7] #Orbital period of the binary stars
    return (binary_time, binary_eccentricity, binary_semi_major_axis, 
            binary_semi_major_crit, binary_orbital_period, colores[color])
#Defining a function that'll call in all parameters of the cbp
def cast_simulation_cbp(file, color):
    cbp_data = np.genfromtxt(file) #Chooses the cbp
    cbp_time = cbp_data[:,0] #Time axis of cbp file
    cbp_eccentricity = cbp_data[:,5] #Eccentricity axis of cbp file
    cbp_semi_major_axis = cbp_data[:,1] #Semi-major axis of cbp
    cbp_insolation = cbp_data[:,-1] #Insolation of cbp
    return (cbp_time, cbp_eccentricity, cbp_semi_major_axis, cbp_insolation,
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

#Plotting the insolation of the cbp on the top panel
axes[0].plot(cbp[0], cbp[3], lw=3, color = planet_color_sim, ls = "-", label = "CBP")
axes[0].set_xscale("log")
axes[0].set_xlabel("Time [yr]")
axes[0].set_xlim(xmin=1e+6)
axes[0].set_ylim(ymin=0.3, ymax = 1.3)
axes[0].set_ylabel("Insolation " + r"$[I/I_{\oplus}]$")

#Plotting the semi-major axis of the cbp and a_crit on the middle panel
axes[1].plot(cbp[0], cbp[2], lw=3, color = planet_color_sim, 
             ls = "-", label = "Simulated CBP") #Semi-major axis of the cbp
axes[1].plot(star[0], star[3], lw=3, color = acrit_color, 
             ls = "--", label = "Simulated " + r"$a_{crit}$") #a_crit
axes[1].set_xscale("log")
axes[1].set_xlabel("Time [yr]")
axes[1].set_xlim(xmin=1e+6)
axes[1].set_ylabel("Semi-Major axis [AU]")
axes[1].legend(loc = (0, .3))

#Plotting the free eccentricity of the cbp
axes[2].plot(cbp[0], cbp[1], lw=3, color = planet_color_sim, 
             ls = "-", label = "Simulated " + r"$e_{free}$")
axes[2].set_xscale("log")
axes[2].set_xlabel("Time [yr]")
axes[2].set_xlim(xmin=1e+6)
axes[2].set_ylabel("Free Eccentricity")
    
fig.tight_layout()
fig.savefig("habitable_cbp" + ".png")

