
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
mpl.rcParams['figure.figsize'] = (3.3,6)
mpl.rcParams['font.size'] = 6.1

fig, axes = plt.subplots(ncols=1, nrows=3, sharey=False)

data = ["0pt15_StellarMass", "0pt30_StellarMass", 
	"0pt45_StellarMass"]
stellar_mass = ["0.15", "0.30", "0.45"] #Solar mass label
stellar_mass = [x + r"$M_{\odot}$" for x in stellar_mass]

#Defining plot values
lw_plot = 1.1
lw_horizontal = 0.9
lw_vertical = lw_horizontal
fontsize_axis = 9.25
labelsize_tick_params = 8.75
width_tick_params = 1
length_tick_params = 2
for sim in range(len(data)):
    # Load data
    output = vpl.GetOutput(data[sim])
    
    # Extract data
    time = output.secondary.Time
    hz_cbp_rg = output.secondary.HZLimRunaway
    hz_cbp_mg = output.secondary.HZLimMaxGreenhouse
    a_crit = output.secondary.CriticalSemiMajorAxis
    LockTime = output.secondary.LockTime
    for t in range(len(a_crit)):
        if a_crit[t] == max(a_crit):
            t_max = time[t] # Time in which max(a_crit) occurred
            break
    
    if LockTime[-1] < 0:
        LockTime = 0
        print("The stars of " + data[sim] + " never tidally locked during the evolution.")
    else:
        LockTime = LockTime[-1]*1e-6 # converts from Myr to yr
        print("LockTime of " + data[sim] + ":",LockTime)
    
    axes[sim].plot(time, a_crit, lw = lw_plot, 
                   label = r"$a_{crit}$", color = "k", 
                   zorder = 1, rasterized = True)
    
    axes[sim].fill_between(time, hz_cbp_rg, hz_cbp_mg, 
                           where = hz_cbp_rg <= hz_cbp_mg, 
                           color = vpl.colors.pale_blue, 
                           alpha = .5, label = "HZ", 
                           zorder = 0, rasterized = True) # shades pale blue in hz boundaries
    
    if LockTime > 0:
        axes[sim].axvline(LockTime, lw = lw_vertical, 
                          ls = "--", 
                          label = r"$P_{rot}$" + " " + r"$=$" + " " + r"$P_{orb}$", 
                          color = vpl.colors.red, 
                          zorder = 1, rasterized = True)
    else:
        axes[sim].axvline(t_max, lw = lw_vertical, 
                          ls = "--", 
                          label = r"$t(a_{crit,max})$", 
                          color = vpl.colors.red, 
                          zorder = 1, rasterized = True)
        axes[sim].axhline(max(a_crit), lw = lw_horizontal, 
                          ls = "--", label = r"$a_{crit, max}$", 
                          color = vpl.colors.orange, zorder = 2, rasterized = True)

    #Format
    axes[sim].set_xscale("log")
    axes[sim].set_xlabel("Time [yr]", fontsize = fontsize_axis)
    axes[sim].set_xlim(1e+7, time.max())
    axes[sim].set_ylabel("Semi-Major Axis [AU]", fontsize = fontsize_axis)
    axes[sim].set_xticks([10**(i + 5) for i in range(6)])
    axes[sim].tick_params(axis = 'both', which = 'major', 
                          labelsize = labelsize_tick_params, 
                          width = width_tick_params, 
                          length = length_tick_params)
    axes[sim].annotate(stellar_mass[sim], (0.05, 0.05), 
                       xycoords = 'axes fraction', fontsize = 15)

#Individual Formatting
axes[0].set_ylim(0.07, 0.24)
axes[0].set_yticks([0.04*i + 0.08 for i in range(5)])
axes[1].set_ylim(0.14, 0.35)
axes[1].set_yticks([0.05*i + 0.15 for i in range(5)])
axes[2].set_ylim(0.14, 0.55)
axes[2].set_yticks([0.10*i + 0.15 for i in range(5)])

axes[2].legend(loc = "upper left")

for sim in range(len(data)):
    axes[sim].set_rasterization_zorder(0)

fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('HZ_Evolution.pdf', bbox_inches="tight", 
                dpi = 200)
if (sys.argv[1] == 'png'):
    plt.savefig('HZ_Evolution.png', bbox_inches="tight", 
                dpi = 200)

