
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
mpl.rcParams['figure.figsize'] = (36,27)
mpl.rcParams['font.size'] = 22.0

# Load data
output = vpl.GetOutput()

# Extract data
time = output.cbp.Time
ecc_cbp = output.cbp.Eccentricity
a_cbp = output.cbp.CBPR #Semi-major axis of the cbp
insol_cbp = output.cbp.CBPInsol # Insolation of the cbp

a_crit = output.secondary.CriticalSemiMajorAxis

#Plot
fig, axes = plt.subplots(ncols=1, nrows=3, sharey=False)
fig.set_size_inches(16,22)

# Each line gets it own color
planet_color = vpl.colors.pale_blue
acrit_color = "k" #black

##Plotting the insolation of the cbp on the top panel##
axes[0].plot(time, insol_cbp, lw=3, 
             color = planet_color, ls = "-", 
             label = "CBP")

#Format
axes[0].set_xscale("log")
axes[0].set_xlabel("Time [yr]")
axes[0].set_xlim(1e+6, time.max())
axes[0].set_ylim(ymin=0.3, ymax = 1.3)
axes[0].set_ylabel("Insolation " + r"$[I/I_{\oplus}]$")

##Plotting the semi-major axis of the cbp and a_crit on the middle panel##
axes[1].plot(time, a_cbp, lw=3, 
             color = planet_color, ls = "-", 
             label = "Simulated CBP") #Semi-major axis of the cbp
axes[1].plot(time, a_crit, lw=3, 
             color = acrit_color, ls = "--", 
             label = "Simulated " + r"$a_{crit}$") #a_crit

#Format
axes[1].set_xscale("log")
axes[1].set_xlabel("Time [yr]")
axes[1].set_xlim(1e+6, time.max())
axes[1].set_ylabel("Semi-Major axis [AU]")
axes[1].legend(loc = (0, 0.35))

##Plotting the free eccentricity of the cbp##
axes[2].plot(time, ecc_cbp, lw=3, 
             color = planet_color, ls = "-", 
             label = "Simulated " + r"$e_{free}$")

#Format
axes[2].set_xscale("log")
axes[2].set_xlabel("Time [yr]")
axes[2].set_xlim(1e+6, time.max())
axes[2].set_ylabel("Eccentricity")
    
fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('habitable_cbp.pdf', bbox_inches="tight")
if (sys.argv[1] == 'png'):
    plt.savefig('habitable_cbp.png', bbox_inches="tight")

