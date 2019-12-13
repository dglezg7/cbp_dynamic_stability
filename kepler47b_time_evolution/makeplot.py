
# coding: utf-8

# In[1]:

from __future__ import division, print_function

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import vplot as vpl
import sys

output = vpl.GetOutput()

"""

# Check correct number of arguments
if (len(sys.argv) != 2):
    print('ERROR: Incorrect number of arguments.')
    print('Usage: '+sys.argv[0]+' <pdf | png>')
    exit(1)
if (sys.argv[1] != 'pdf' and sys.argv[1] != 'png'):
    print('ERROR: Unknown file format: '+sys.argv[1])
    print('Options are: pdf, png')
    exit(1)

"""
    
#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (18,15)
mpl.rcParams['font.size'] = 22.0

# Load data
output = vpl.GetOutput()

# Extract data
time = output.cbp.Time
ecc_cbp = output.cbp.Eccentricity
a_cbp = output.cbp.CBPR #Semi-major axis of the cbp

ecc_star = output.secondary.Eccentricity #By star we mean specifically the secondary star
a_star = output.secondary.SemiMajorAxis
a_crit = output.secondary.CriticalSemiMajorAxis
OrbP_star = output.secondary.OrbPeriod

#Plot
fig, axes = plt.subplots(ncols=2, nrows=2, sharey=False)
fig.set_size_inches(18,12)

# Each line gets it own color
star_color_sim = vpl.colors.orange
star_color_obs = vpl.colors.purple
planet_color_sim = vpl.colors.pale_blue
planet_color_obs = vpl.colors.red
acrit_color = "k" #black

#Observed values of the Kepler 47 binary star system
observed_k47_semi_major_axis = 0.0836 # In AU
observed_k47_orbital_period = 7.44837695 # In days
observed_k47_ecc = 0.0234
observed_cbp_semi_major_axis = 0.2956 # In AU
observed_cbp_ecc = 0.035

#Creating an array for the observed values in order for the values to match the time array
def time_array(Time, observed_value):
    return [observed_value for i in range(len(Time))]
obs_k47_a = time_array(time, observed_k47_semi_major_axis)
obs_k47_OrbP = time_array(time, observed_k47_orbital_period)
obs_k47_ecc = time_array(time, observed_k47_ecc)
obs_k47_cbp_a = time_array(time, observed_cbp_semi_major_axis)
obs_cbp_ecc = time_array(time, observed_cbp_ecc)


##Plotting the simulated and observed semi-major axis of the star on the top-left panel##
axes[0,0].plot(time, a_star, lw=3, 
               color = star_color_sim, ls = "-", 
               label = "Simulated " + r"$a_{47B}$") #Simulated K47B data
axes[0,0].plot(time, obs_k47_a, lw=3, 
               color = star_color_obs, ls = "--", 
               label = "Observed " + r"$a_{47B}$") #Observed semi-major axis of K47B

#Format
axes[0,0].set_xscale("log")
axes[0,0].set_xlabel("Time [yr]")
axes[0,0].set_xlim(1e+6, time.max())
axes[0,0].set_ylim(.0805, .085)
axes[0,0].set_ylabel("Semi-Major axis [AU]")

##Plotting the simulated and observed semi-major axis of the cbp on the top-right panel##
axes[0,1].plot(time, a_cbp, lw=3, 
               color = planet_color_sim, ls = "-", 
               label = "K-47b simulated") #Simulated K47b data
axes[0,1].plot(time, obs_k47_cbp_a, lw=3, 
               color = planet_color_obs, ls = "--", 
               label = "K-47b observed") #Observed semi-major axis of K47b
axes[0,1].plot(time, a_crit, lw=3, 
               color = acrit_color, ls = "--", 
               label = "Simulated " + r"$a_{crit}$") #Simulated a_crit

#Format
axes[0,1].set_xscale("log")
axes[0,1].set_xlabel("Time [yr]")
axes[0,1].set_xlim(1e+6, time.max())
axes[0,1].set_ylim(0.205, 0.315)
axes[0,1].set_ylabel("Semi-Major axis [AU]")
axes[0,1].legend(loc = (0.35, 0.25))

##Plotting the simulated and observed binary eccentricity of the star on the bottom-left panel##
axes[1,0].plot(time, ecc_star, lw=3, 
               color = star_color_sim, ls = "-", 
               label = "K-47B simulated") #Simulated K47B data
axes[1,0].plot(time, obs_k47_ecc, lw=3, 
               color = star_color_obs, ls = "--", 
               label = "K-47B observed") #Observed binary eccentricity of K47B

#Format
axes[1,0].set_xscale("log")
axes[1,0].set_xlabel("Time [yr]")
axes[1,0].set_xlim(1e+6, time.max())
axes[1,0].set_ylim(0.01, 0.11)
axes[1,0].set_ylabel("Binary Eccentricity")
axes[1,0].legend(loc = "center left")

##Plotting the simulated and observed free eccentricity of the cbp on the bottom-right panel##
axes[1,1].plot(time, ecc_cbp, lw=3, 
               color = planet_color_sim, ls = "-", 
               label = "Simulated " + r"$e_{free, 47b}$") #Simulated K47b data
axes[1,1].plot(time, obs_cbp_ecc, lw=3, 
               color = planet_color_obs, ls = "--", 
               label = "Observed " + r"$e_{free, 47b}$") #Observed free eccentricity of K47b

#Format
axes[1,1].set_xscale("log")
axes[1,1].set_xlabel("Time [yr]")
axes[1,1].set_xlim(1e+6, time.max())
axes[1,1].set_ylim(0.005, 0.08)
axes[1,1].set_ylabel("CBP Eccentricity")
 
fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('kepler47.pdf', bbox_inches="tight")
if (sys.argv[1] == 'png'):
    plt.savefig('kepler47.png', bbox_inches="tight")

