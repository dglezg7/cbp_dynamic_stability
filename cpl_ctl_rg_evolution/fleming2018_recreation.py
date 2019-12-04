
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import astropy.units as u
import sympy as sp
from sympy import *

#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (18,15)
mpl.rcParams['font.size'] = 22.0

fig, axes = plt.subplots(ncols=3, nrows=1, sharey=False)
fig.set_size_inches(36,12)

# Each line gets it own color
colores = ["C" + str(n) for n in range(6)]

#Since this data is not generalized nor looped, I will be very specific about the values written on here

fleming2018 = "fleming2018" #First part of all files in this folder
primary = ".primary.forward" #Calls primary star
secondary = ".secondary.forward" #Calls secondary star
str_cpl_rg_off = "cpl_rg_off"
str_cpl_rg_on = "cpl_rg_on"
str_ctl_rg_off = "ctl_rg_off"
str_ctl_rg_on = "ctl_rg_on"


#We'll define a function that'll call in all parameters of the secondary star
def cast_simulation(sim_name, color):
    binary_data = np.genfromtxt(fleming2018 + "_" + sim_name + secondary) #Chooses the secondary star
    binary_time = binary_data[:,0] #Time axis of each secondary binary file
    binary_eccentricity = binary_data[:,6] #Eccentricity axis of each secondary binary file
    binary_semi_major_axis = binary_data[:,3] #Semi-major axis of secondary star
    binary_semi_major_crit = binary_data[:,10] #Critical semi-major axis of the binary stars
    binary_orbital_period = binary_data[:,7] #Orbital period of the binary stars
    return (binary_time, binary_eccentricity, binary_semi_major_axis, 
            binary_semi_major_crit, binary_orbital_period, colores[color])

cpl_rg_off = cast_simulation(str_cpl_rg_off, 0) #Defines every needed data to plot the values
cpl_rg_on = cast_simulation(str_cpl_rg_on, 1)
ctl_rg_on = cast_simulation(str_ctl_rg_on, 2)
ctl_rg_off = cast_simulation(str_ctl_rg_off, 3)

#Plotting the values
#We'll plot semi-major axis on the top first

axes[0].plot(cpl_rg_off[0], cpl_rg_off[3], lw=3, color = cpl_rg_off[5], ls = "-", label = "CPL, RG evolution: off")
axes[0].plot(cpl_rg_on[0], cpl_rg_on[3], lw=3, color = cpl_rg_on[5], ls = "-", label = "CPL, RG evolution: on")
axes[0].plot(ctl_rg_on[0], ctl_rg_on[3], lw=3, color = ctl_rg_on[5], ls = "--", label = "CTL, RG evolution: on")
axes[0].plot(ctl_rg_off[0], ctl_rg_off[3], lw=3, color = ctl_rg_off[5], ls = "--", label = "CTL, RG evolution: off")
axes[0].set_xscale("log")
axes[0].set_xlabel("Time [yr]", size = 30)
axes[0].set_xlim(xmin=1e+5)
axes[0].set_ylim(ymin=0.145, ymax = 0.34)
axes[0].set_ylabel("Critical Semi-Major Axis [AU]", size = 30)
axes[0].tick_params(axis = 'both', which = 'major', labelsize = 24)
axes[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
axes[0].legend(loc = "upper right")

#The star's orbital period goes in the middle
axes[1].plot(cpl_rg_off[0], cpl_rg_off[4], lw=3, color = cpl_rg_off[5], ls = "-", label = "CPL, RG evolution: off")
axes[1].plot(cpl_rg_on[0], cpl_rg_on[4], lw=3, color = cpl_rg_on[5], ls = "-", label = "CPL, RG evolution: on")
axes[1].plot(ctl_rg_on[0], ctl_rg_on[4], lw=3, color = ctl_rg_on[5], ls = "--", label = "CTL, RG evolution: on")
axes[1].plot(ctl_rg_off[0], ctl_rg_off[4], lw=3, color = ctl_rg_off[5], ls = "--", label = "CTL, RG evolution: off")
axes[1].set_xscale("log")
axes[1].set_xlabel("Time [yr]", size = 30)
axes[1].set_xlim(xmin=1e+5)
axes[1].set_ylabel("Orbital Period [days]", size = 30)
axes[1].tick_params(axis = 'both', which = 'major', labelsize = 24)

#The eccentricity is the plot on very right"
axes[2].plot(cpl_rg_off[0], cpl_rg_off[1], lw=3, color = cpl_rg_off[5], ls = "-", label = "CPL, RG evolution: off")
axes[2].plot(cpl_rg_on[0], cpl_rg_on[1], lw=3, color = cpl_rg_on[5], ls = "-", label = "CPL, RG evolution: on")
axes[2].plot(ctl_rg_on[0], ctl_rg_on[1], lw=3, color = ctl_rg_on[5], ls = "--", label = "CTL, RG evolution: on")
axes[2].plot(ctl_rg_off[0], ctl_rg_off[1], lw=3, color = ctl_rg_off[5], ls = "--", label = "CTL, RG evolution: off")
axes[2].set_xscale("log")
axes[2].set_xlabel("Time [yr]", size = 30)
axes[2].set_xlim(xmin=1e+5)
axes[2].set_ylabel("Eccentricity", size = 30)
axes[2].tick_params(axis = 'both', which = 'major', labelsize = 24)

fig.tight_layout()
fig.savefig("fleming2018_with_ctl" + ".png", bbox_inches="tight")

