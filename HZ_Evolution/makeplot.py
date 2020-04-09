
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

#Time (in seconds) when body stars tidally locked (identical stars lock at the same time)
sec_to_yrs = (3600*24*365)**(-1)
lock_0pt15 = 1.062805e+16 * sec_to_yrs
lock_0pt30 = 6.288010e+15 * sec_to_yrs
lock_0pt45 = 4.205003e+15 * sec_to_yrs
tidal_lock_times = [lock_0pt15, lock_0pt30, lock_0pt45]

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

    axes[sim].plot(time, a_crit, lw = lw_plot, 
                   label = r"$a_{crit}$", color = "k", 
                   zorder = 1, rasterized = True)
    
    axes[sim].fill_between(time, hz_cbp_rg, hz_cbp_mg, 
                           where = hz_cbp_rg <= hz_cbp_mg, 
                           color = vpl.colors.pale_blue, 
                           alpha = .5, label = "HZ", 
                           zorder = 0, rasterized = True) # shades pale blue in hz boundaries
    axes[sim].axvline(tidal_lock_times[sim], lw = lw_vertical, 
                      ls = "--", 
                      label = r"$P_{rot}$" + " " + r"$=$" + " " + r"$P_{orb}$", 
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

#Individual Formatting
axes[0].set_ylim(0.07, 0.24)
axes[0].set_yticks([0.04*i + 0.08 for i in range(5)])
axes[1].set_ylim(0.14, 0.35)
axes[1].set_yticks([0.05*i + 0.15 for i in range(5)])
axes[2].set_ylim(0.14, 0.55)
axes[2].set_yticks([0.10*i + 0.15 for i in range(5)])

axes[0].legend(loc = "lower left")

for sim in range(len(data)):
    axes[sim].set_rasterization_zorder(0)

fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('HZ_Evolution.pdf', bbox_inches="tight", 
                dpi = 200)
if (sys.argv[1] == 'png'):
    plt.savefig('HZ_Evolution.png', bbox_inches="tight", 
                dpi = 200)

