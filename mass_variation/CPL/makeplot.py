
# coding: utf-8

# In[ ]:




# In[ ]:

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
mpl.rcParams['figure.figsize'] = (3.45,6)
mpl.rcParams['font.size'] = 4.8

#Plot
nrows = 3
fig, axes = plt.subplots(ncols = 1, nrows = nrows, sharey=False)

#Making an array of all folders in order to extract the data from each folder
mass_range = ["0." + str(1 + 2*i) 
             for i in range(5)] #Stores a range of masses of K47A/B

mass_folder_names = ['M' + M.replace('.', 'pt') for M in mass_range]
data = mass_folder_names

mass_labels = [i + r"$M_{\odot}$" for i in mass_range]

#Colorblind-proof VPL colors for each dataset. Assigning CPL model to warm colors and CTL to cool colors.
colors = [vpl.colors.red, vpl.colors.orange, 
          vpl.colors.pale_blue, vpl.colors.dark_blue, 
          vpl.colors.purple]

#Defining plot values
lw_plot = 1.1
fontsize_axis = 7.25
labelsize_tick_params = 8
width_tick_params = 0.36
length_tick_params = 1.1

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
        
    label = r"M = " + mass_labels[sim]
    
    #Plotting the critical semi-major axis
    axes[0].plot(time, a_crit, lw = lw_plot, 
                 label = label, color = colors[sim])
    
    #Plotting the orbital period
    axes[1].plot(time, orbP, lw = lw_plot, 
                 label = label, color = colors[sim])
    
    #Plotting the binary eccentricity
    axes[2].plot(time, ecc, lw = lw_plot, 
                 label = label, color = colors[sim]) 
    
#Formats that are unique to each plot

#Fomatting a_crit
axes[0].set_ylabel("Critical Semi-Major Axis [AU]", 
                   size = fontsize_axis)
axes[0].set_ylim(ymin = 0.10, ymax = 0.28)
axes[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

#Formatting the orbital period
axes[1].set_ylabel("Orbital Period [days]", 
                   size = fontsize_axis)
axes[1].set_ylim(ymin = 3.4 ,ymax = 7.0)

#formatting the binary eccentricity
axes[2].set_ylabel("Eccentricity", 
                   size = fontsize_axis)
axes[2].set_ylim(ymin = -0.01 ,ymax = 0.28)
axes[2].legend(loc = "lower left", ncol = 3)

#Looping some formats that will be the same on all three plots
for n in range(nrows):
    axes[n].set_xscale("log")
    axes[n].set_xlabel("Time [yr]", size = fontsize_axis)
    axes[n].set_xlim(1e+4, time.max())
    axes[n].tick_params(axis = 'both', which = 'major', 
                        labelsize = labelsize_tick_params, 
                        width = width_tick_params, 
                        length = length_tick_params)
    axes[n].set_rasterization_zorder(0)

fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('masses_CPL.pdf', bbox_inches="tight", 
                dpi = 200)
if (sys.argv[1] == 'png'):
    plt.savefig('masses_CPL.png', bbox_inches="tight",
               dpi = 200)

