
# coding: utf-8

# In[ ]:

from __future__ import division, print_function

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import vplot as vpl
import sys

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
mpl.rcParams['figure.figsize'] = (4.2,6)
mpl.rcParams['font.size'] = 5.2

# Load data
output = vpl.GetOutput()

# Extract data
time = output.cbp.Time
ecc_cbp = output.cbp.Eccentricity
a_cbp = output.cbp.CBPR #Semi-major axis of the cbp
instell_cbp = output.cbp.Instellation # Incident stellar radiation on the cbp
sol_const = 1361 #Solar Constant, average incident flux the Earth receives [W/m^2]
instell_cbp_Earth = instell_cbp / sol_const #Instellation of cpb in Earth units

a_crit = output.secondary.CriticalSemiMajorAxis

#Plot
nrows = 3
fig, axes = plt.subplots(ncols = 1, nrows = nrows, sharey=False)

# Each line gets it own color
planet_color = vpl.colors.pale_blue
acrit_color = "k" #black
a_critMax_color = vpl.colors.orange

#Defining plot values
lw_plot = 1.2
lw_horizontal = 1.5
fontsize_axis = 9
labelsize_tick_params = 7.7
width_tick_params = 0.9
length_tick_params = 2.9

##Plotting the insolation of the cbp on the top panel##
axes[0].plot(time, instell_cbp_Earth, lw = lw_plot, 
             color = planet_color, ls = "-", 
             label = "CBP", rasterized = True)

#Format
axes[0].set_ylim(ymin=0.45, ymax = 0.9)
axes[0].set_ylabel("Instellation " + "[Earth Units]", 
                   fontsize = fontsize_axis) 

##Plotting the semi-major axis of the cbp and a_crit on the middle panel##
axes[1].plot(time, a_cbp, lw = lw_plot, 
             color = planet_color, ls = "-", 
             label = "CBP", rasterized = True) #Semi-major axis of the cbp
axes[1].plot(time, a_crit, lw = lw_plot, 
             color = acrit_color, ls = "-", 
             label = r"$a_{crit}$", rasterized = True) #a_crit
axes[1].axhline(max(a_crit), lw = lw_horizontal, 
                color = a_critMax_color, ls = "--", 
                label = r"$a_{crit, max}$", rasterized = True) #Maximum a_crit

#Format
axes[1].set_ylim(0.157, 0.3)
axes[1].set_ylabel("Semi-Major Axis [AU]", 
                   fontsize = fontsize_axis)
axes[1].set_yticks([0.02*i + 0.16 for i in range(8)]) 
axes[1].legend(loc = "lower left")

##Plotting the free eccentricity of the cbp##
axes[2].plot(time, ecc_cbp, lw = lw_plot, 
             color = planet_color, ls = "-", 
             label = r"$e_{free}$", rasterized = True)

#Format
axes[2].set_ylim(0.037, 0.16)
axes[2].set_ylabel("Eccentricity", 
                   fontsize = fontsize_axis)

#Looping some formats that will be the same on all three plots
for n in range(nrows):
    axes[n].set_xscale("log")
    axes[n].set_xlabel("Time [yr]", fontsize = fontsize_axis)
    axes[n].set_xlim(1e+6, time.max())
    axes[n].tick_params(axis = 'both', which = 'major', 
                        labelsize = labelsize_tick_params,
                        width = width_tick_params, 
                        length = length_tick_params)
    axes[n].set_rasterization_zorder(0)
    
fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('HabitableCBP.pdf', bbox_inches="tight", 
                dpi = 200)
if (sys.argv[1] == 'png'):
    plt.savefig('HabitableCBP.png', bbox_inches="tight", 
                dpi = 200)

