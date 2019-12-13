
# coding: utf-8

# In[11]:

from __future__ import division, print_function

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
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
mpl.rcParams['figure.figsize'] = (18,15)
mpl.rcParams['font.size'] = 22.0

#Plot
fig, axes = plt.subplots(ncols=3, nrows=1, sharey=False)
fig.set_size_inches(36,12)

#Making an array of all folders in order to extract the data from each folder
data = ["fleming2018_cpl_rg_off", "fleming2018_cpl_rg_on", 
        "fleming2018_ctl_rg_off", "fleming2018_ctl_rg_on"]

#Colorblind-proof VPL colors for each dataset. Assigning CPL model to warm colors and CTL to cool colors.
colors = [vpl.colors.red, vpl.colors.orange,
          vpl.colors.purple, vpl.colors.pale_blue]

#Extracting and plotting the data from each folder
for sim in range(len(data)):
    # Load data
    output = vpl.GetOutput(data[sim])
    
    # Extract data
    time = output.secondary.Time 
    a_crit = output.secondary.CriticalSemiMajorAxis
    orbP = output.secondary.OrbPeriod
    ecc = output.secondary.Eccentricity
    
    """
    Plotting semi-major axis on the top first, orbital period in the middle, 
    and then the eccentricity on the bottom panel
    """
    
    cpl_bool = "cpl" in data[sim] #defines whether model used was CPL or CTL
    rg_bool = "on" in data[sim] #defines whether RG evolution was on or off
    
    #Making the plot label and linestyle for each simulation. Solid for CPL and dashed for CPL
    if cpl_bool == True:
        model = "CPL"
        ls = "-" #linestyle is solid
    elif cpl_bool == False:
        model = "CTL"
        ls = "--" #linestyle is dashed
    
    #Including in the plot label whether the RG evolution was on or not
    if rg_bool == True:
        rg_evolution = "on"
    elif rg_bool == False:
        rg_evolution = "off"
        
    label = model + ", RG evolution: " + rg_evolution
    
    #Plotting the critical semi-major axis
    axes[0].plot(time, a_crit, lw=3, ls = ls, label = label, color = colors[sim])
    
    #Plotting the orbital period
    axes[1].plot(time, orbP, lw=3, ls = ls, label = label, color = colors[sim])
    
    #Plotting the binary eccentricity
    axes[2].plot(time, ecc, lw=3, ls = ls, label = label, color = colors[sim])
    
#Looping some formats that will be the same on all three plots
for i in range(3):
    axes[i].set_xscale("log")
    axes[i].set_xlabel("Time [yr]", size = 30)
    axes[i].set_xlim(1e+5, time.max())
    axes[i].tick_params(axis = 'both', which = 'major', labelsize = 24)
    
#Formats that are unique to each plot

#Fomatting a_crit
axes[0].set_ylabel("Critical Semi-Major Axis [AU]", size = 30)
axes[0].set_ylim(ymin=0.1525, ymax = 0.35)
axes[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
axes[0].legend(loc = "upper right")

#Formatting the orbital period
axes[1].set_ylabel("Orbital Period [days]", size = 30)
axes[1].set_ylim(ymin=4.25 ,ymax=8)

#formatting the binary eccentricity
axes[2].set_ylabel("Binary Eccentricity", size = 30)
axes[2].set_ylim(ymin=-0.01 ,ymax=0.32)

fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('fleming2018_with_ctl.pdf', bbox_inches="tight")
if (sys.argv[1] == 'png'):
    plt.savefig('fleming2018_with_ctl.png', bbox_inches="tight")

