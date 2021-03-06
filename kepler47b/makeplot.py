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
mpl.rcParams['figure.figsize'] = (6,3.85)
mpl.rcParams['font.size'] = 6
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
ncols = 2
nrows = 2
fig, axes = plt.subplots(ncols = ncols, nrows = nrows, sharey=False)

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

#Defining plot values
lw_plot = 1
lw_horizontal = 1.2
fontsize_axis = 6.9
labelsize_tick_params = 7.5
width_tick_params = 0.3
length_tick_params = 1.3


##Plotting the simulated and observed semi-major axis of the star on the top-left panel##
axes[0,0].plot(time, a_star, lw = lw_plot, 
               color = star_color_sim, ls = "-", 
               label = "Simulation", rasterized = True) #Simulated K47B data
axes[0,0].axhline(observed_k47_semi_major_axis, 
                  lw = lw_horizontal, 
                  color = star_color_obs, ls = "-", 
                  label = "Observation", rasterized = True) #Observed semi-major axis of K47B

#Format
axes[0,0].set_ylim(.0819, .0852)
axes[0,0].set_ylabel("Star Semi-Major axis [AU]", 
                     fontsize = fontsize_axis)

##Plotting the simulated and observed semi-major axis of the cbp on the top-right panel##
axes[0,1].plot(time, a_cbp, lw = lw_plot, 
               color = planet_color_sim, ls = "-", 
               label = "Simulation", rasterized = True) #Simulated K47b data
axes[0,1].axhline(observed_cbp_semi_major_axis, 
                  lw = lw_horizontal, 
                  color = planet_color_obs, ls = "-", 
                  label = "Observation", rasterized = True) #Observed semi-major axis of K47b
axes[0,1].plot(time, a_crit, lw = lw_plot, 
               color = acrit_color, ls = "-", 
               label = r"$a_{crit}$", rasterized = True) #Simulated a_crit

#Format
axes[0,1].set_ylim(0.195, 0.32)
axes[0,1].set_ylabel("CBP Semi-Major Axis [AU]", 
                     fontsize = fontsize_axis)
axes[0,1].legend(loc = (0.01, 0.31))

##Plotting the simulated and observed binary eccentricity of the star on the bottom-left panel##
axes[1,0].plot(time, ecc_star, lw = lw_plot, 
               color = star_color_sim, ls = "-", 
               label = "Simulation", rasterized = True) #Simulated K47B data
axes[1,0].axhline(observed_k47_ecc, 
                  lw = lw_horizontal, 
                  color = star_color_obs, ls = "-", 
                  label = "Observation", rasterized = True) #Observed binary eccentricity of K47B

#Format
axes[1,0].set_ylim(0.01, 0.11)
axes[1,0].set_ylabel("Binary Eccentricity", 
                     fontsize = fontsize_axis)
axes[1,0].legend(loc = "center left")

##Plotting the simulated and observed free eccentricity of the cbp on the bottom-right panel##
axes[1,1].plot(time, ecc_cbp, lw = lw_plot, 
               color = planet_color_sim, ls = "-", 
               label = "Simulation", rasterized = True) #Simulated K47b data
axes[1,1].axhline(observed_cbp_ecc, 
                  lw = lw_horizontal, 
                  color = planet_color_obs, ls = "-", 
                  label = "Observation", rasterized = True) #Observed free eccentricity of K47b

#Format
axes[1,1].set_ylim(-0.002, 0.08)
axes[1,1].set_ylabel("CBP Eccentricity", 
                     fontsize = fontsize_axis)

for r in range(nrows):
    for c in range(ncols):
        axes[r,c].set_xscale("log")
        axes[r,c].set_xlabel("Time [yr]", 
                             fontsize = fontsize_axis)
        axes[r,c].set_xlim(1e+6, time.max())
        axes[r,c].tick_params(axis = 'both', which = 'major', 
                              labelsize = labelsize_tick_params, 
                              width = width_tick_params, 
                              length = length_tick_params)
        axes[r,c].set_rasterization_zorder(0) 
 
fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('kepler-47b.pdf', bbox_inches="tight", 
                dpi = 200)
if (sys.argv[1] == 'png'):
    plt.savefig('kepler-47b.png', bbox_inches="tight", 
                dpi = 200)

