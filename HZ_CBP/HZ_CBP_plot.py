
# coding: utf-8

# In[ ]:

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.interpolate import interp1d
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
mpl.rcParams['figure.figsize'] = (9,7.5) #It was originally (9,7.5)
mpl.rcParams['font.size'] = 22.0 #It was originally 22.0

fig, axes = plt.subplots(ncols=1, nrows=1, sharey=False)
fig.set_size_inches(21,12)

# 1D Interpolations to Baraffe et al., 2015 stellar models
baraffe2015MArr = np.array([0.1, 0.11, 0.13, 0.15, 0.17, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1])


# Teff at 4.5e9 yr old
baraffe2015TeffMSArr = np.array([2811, 2916, 3046, 3131, 3192, 3262, 3521, 3981, 4424, 4887, 5310, 5713, 5997])


# L/Lsun at 4.5e9 yr old
baraffe2015LMSArr = np.power(10,np.array([-3.062, -2.924, -2.727, -2.58, -2.462, -2.317, -1.707, -1.148, -.841, -.553, -.281, -.011, .253]))

# 1D interpolation to build functions that takes stellar mass in Msun as
# input and outputs Teff [K] or L [Lsun], respectively
fTeffMS = interp1d(baraffe2015MArr, baraffe2015TeffMSArr, kind = "quadratic")
fLMS = interp1d(baraffe2015MArr, baraffe2015LMSArr, kind = "quadratic")

some_mass_values = np.arange(.1, 1.1, 1e-2) #Defined an array of solar mass values from 0.1 to 1.1 solar masses
Teff = fTeffMS(some_mass_values)
L = fLMS(some_mass_values)


# # Finding HZ limits by using Kopparapu 2013 equations
# 
# $$S_{eff} = S_{eff \odot} + aT + bT^2 +cT^3 +dT^4$$
# Where $T = T_{eff} - 5780$
# And HZ limits are defined by the distance relating to the luminosity of the binary star system of equal masses
# We want
# $$d = \sqrt{\frac{2L/L_{\odot}}{S_{eff}}}$$
# 
# # Then we see how $a_{crit}$ crosses over the HZ by using Holman & Wiegert's $a_{crit}$ equation
# 
# $$a_{crit} = (1.6 + 5.1e - 2.22e^2 + 4.12\mu - 4.27e\mu - 5.09\mu^2 + 4.61e\mu^2)a_{star}$$
# 
# Where $\mu = .5$ for equal-mass stars, e will range, and $a_{star}$ depends on kepler's third law with $P_{orb} = 7.5 days$


"""rg = runaway greenhouse, mg = maximum greenhouse, S = effective stellar flux, T = temperature"""
S_rg = 1.0512
a_rg = 1.3242e-4
b_rg = 1.5418e-8
c_rg = -7.9895e-12
d_rg = -1.8328e-15

S_mg = 0.3438
a_mg = 5.8942e-5
b_mg = 1.6558e-9
c_mg = -3.0045e-12
d_mg = -5.2983e-16
#S, a, b, c, and d values are constants obtained from Table 3 of Kopparapu 2013. 

def T_star(T_eff): #Defining the effective temperature
    return T_eff - 5780

def S_eff(S, a, b, c, d, T): #Defining the effective stellar flux
    return S + a*T + b*T**2 + c*T**3 + d*T**4

"""HZ = Habitable Zone, cbp = circumbinary planet, L = luminosity, M = mass"""
def hz_cbp_distance(S, L_sun_ratio): #Defining the function of the hz for two tight orbiting binary stars.
    return np.sqrt(2 * L_sun_ratio / S) #Strictly considering two identical stars

T_star = T_star(Teff) #Array of effective star temperature dervied from 1D interpolation
S_eff_rg = S_eff(S_rg, a_rg, b_rg, c_rg, d_rg, T_star) #Effective stellar flux at inner boundary
S_eff_mg = S_eff(S_mg, a_mg, b_mg, c_mg, d_mg, T_star) #Effective stellar flux at outer boundary
hz_cbp_rg = hz_cbp_distance(S_eff_rg, L) #Inner boundary of the hz
hz_cbp_mg = hz_cbp_distance(S_eff_mg, L) #Outer boundary of the hz

#Creating the critical semi-major axis fit

def holman_wiegert_a_crit(mu, e, a): #e: binary eccentricity. a: binary semi major axis, where a is an array
    """
    e: binary eccentricity. a: binary semi major axis, where a is an array
    mu: mass ratio, where mu always equals 0.5 for equal mass binary stars.
    """
    output = np.empty(len(a))
    for i in range(len(a)):
        output[i] = (1.6 + 5.1*e - 2.22*e**2 + 4.12*mu - 4.27*e*mu - 5.09*mu**2 + 4.61*(e*mu)**2)*a[i]
    return output

#Use Kepler's third law to depend stellar mass with semi-major axis
def k3(M1, M2, P):
    """
    Output will be an array of semi-major axis values from the inputs of both star masses
    and the orbital period. In our case, the orbital period is strictly 7.5 days while the
    array of M1 and M2 two will be the identical array that we used to input into the 
    1D interpolation function. 0.1 M_sun < M1, M2 < 1.1 M_sun
    """
    #days to seconds for the orbital period
    days_to_sec = 24*3600
    #Solar masses to kg for the M values
    sol_to_kg = 2e30
    #Meters to AU
    m_to_AU = 1/(150e9)
    G = 6.67e-11 #In m**3/(kg*s**2)
    #Obtaining semi-major axis in AU units
    if len(M1) == len(M2):
        a = np.empty(len(M1))
        for i in range(len(M1)):
            a[i] = m_to_AU*(G*(M1[i] + M2[i])*sol_to_kg*(P*days_to_sec)**2/(4*np.pi**2))**(1/3)
    else:
        print("Güey, did you check to see if len(M1) == len(M2)??")
    return a

#Defining the a_crit values for each eccentricity 
semi_major_axis = k3(some_mass_values, some_mass_values, 7.5) #Equal-mass stars with 7.5 day orbital period
min_a_crit = holman_wiegert_a_crit(.5, 0, semi_major_axis) #a_crit at e = 0.0
a_crit_e_pt1 = holman_wiegert_a_crit(.5, .1, semi_major_axis) #a_crit at e = 0.1
a_crit_e_pt3 = holman_wiegert_a_crit(.5, .3, semi_major_axis) #a_crit at e = 0.3
a_crit_e_pt5 = holman_wiegert_a_crit(.5, .5, semi_major_axis) #a_crit at e = 0.5

#Assigning colors to the habitable zone and the a_crit values
hz_color = vpl.colors.pale_blue
a_crit0_color = "k"
a_crit1_color = vpl.colors.purple
a_crit3_color = vpl.colors.orange
a_crit5_color = vpl.colors.red

##Plotting the a_crit values for each binary eccentricity##
axes.plot(min_a_crit, some_mass_values, lw=4, color = a_crit0_color, 
	  ls = "-", label = r"$a_{crit}$" + " " + r"$(e_{star} = 0.0)$", zorder = 2) #Plots a_crit boundary for e = 0.0
axes.plot(a_crit_e_pt1, some_mass_values, lw=4, color = a_crit1_color, 
          ls = "-", label = r"$a_{crit}$" + " " + r"$(e_{star} = 0.1)$", zorder = 2) #Plots a_crit boundary for e = 0.1
axes.plot(a_crit_e_pt3, some_mass_values, lw=4, color = a_crit3_color, 
          ls = "-", label = r"$a_{crit}$" + " " + r"$(e_{star} = 0.3)$", zorder = 2) #Plots a_crit boundary for e = 0.3
axes.plot(a_crit_e_pt5, some_mass_values, lw=4, color = a_crit5_color, 
          ls = "-", label = r"$a_{crit}$" + " " + r"($e_{star} = 0.5)$", zorder = 2) #Plots a_crit boundary for e = 0.5

##Plotting the habitable zone##
axes.fill_between(hz_cbp_rg, 0, some_mass_values,
                  color = hz_color, alpha = .5, label = "CBP Habitable Zone", zorder = 1) # shades pale blue in hz boundaries
axes.fill_between(hz_cbp_mg, 0, some_mass_values, 
                  color = "white", zorder = 1) #Prevents HZ color from appearing father from outer hz boundary

#Formatting
axes.set_xlabel("Semi-Major Axis" + " [AU] ", size = 34)
axes.set_xticks([0.05*i + 0.1 for i in range(5)])
axes.get_xaxis().set_major_formatter(mticker.ScalarFormatter()) #Removes the logarithmic numbers on x-axis
axes.get_xaxis().set_minor_formatter(mticker.NullFormatter()) #Helps with the above action
axes.tick_params(axis = 'both', which = 'major', labelsize = 28, width=2, length=8)
axes.set_xlim(xmin= 0.1, xmax = 0.3)
axes.set_ylim(ymin=0.105, ymax = 0.5)
axes.set_ylabel("Stellar Mass " + r"$[M_{\odot}]$", size = 34)
axes.legend(loc = "upper left")

fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig('HZ_CBP.pdf', bbox_inches="tight", dpi = 200)
if (sys.argv[1] == 'png'):
    plt.savefig('HZ_CBP.png', bbox_inches="tight", dpi = 200)

