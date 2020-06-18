
# coding: utf-8

# In[1]:

from __future__ import division, print_function

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import vplot as vpl
import sys
import os
import csv
from datetime import datetime

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

start_time = datetime.now()
print(start_time)

#Creating a function in which provides vertical spacing between printed texts
def spprint(value, number_of_spaces):
    print(value)
    if number_of_spaces >= 0 and isinstance(number_of_spaces, int) is True:
        for space in range(number_of_spaces):
            print(" ")
    else:
        print("Check your number of spaces")

#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (3.45,6)
mpl.rcParams['font.size'] = 6.2 

nrows = 3
fig, axes = plt.subplots(ncols = 1, nrows = nrows, sharey = False)

directory = os.getcwd()
files = os.listdir(directory) #makes a list of files in your folder

"""
Since these simulations take a long time to complete, one can already
plot existing data while the simulations are running, therefore the 
coding below plots the existing data and can be refreshed at any time.
"""

existing_ecc_folders = []

#Iterates through all files and folders in "files"
for item in files:
    #If statement below identifies potentially pre-existing simulated folder
    if item.find("e0pt") == 0:
        existing_ecc_folders.insert(len(existing_ecc_folders), item)

#Sorts the existing eccentricities from the smallest to greatest quantities
existing_ecc_folders = sorted(existing_ecc_folders, 
                              key=lambda x: int("".join(
                                  [i for i in x if i.isdigit()])))

#Creates an array of existing initial binary eccentricities in string form with preserved precision
ecc_range = ['{:.3f}'.format(1e-3*float(ecc.split("pt")[1])) 
             for ecc in existing_ecc_folders]

"""
The next section below will open all simulations and extract data
from each simulation in order to place the data inside lists. Each
list will be placed in as a column in a .csv file and will save
all data extracted from the simulations. Loading up all simulations
at once can take up a total between 10 to 20 minutes to create the 
.csv file. This makeplot.py script may be run at the same time the
K47_Eccentricities.py script is creating the data. This also the means
the plot may be updated at any time a new data point is created. Keep 
noted that you should not delete the .csv file. If the .csv file already 
exists, the code will not open all .forward file from each simulation and
will skip directly to plotting the figure.

"""
        
#Creating lists in order to insert the data
eccentricity = [] #Initial eccentricity of the binary stars
a_crit_minus_a_cbp = [] #Max difference between a_crit and a_cbp for all sims are stored here
time_a_crit_equals_a_cbp = [] #time in which a_crit = a_cbp is stored here
Lock_Times_Primary = [] #Stores tidal lock times of all simulations (Myrs)
Lock_Times_Secondary = []

#Throwing all the data together to construct covenience
data = [eccentricity, a_crit_minus_a_cbp, time_a_crit_equals_a_cbp, 
        Lock_Times_Primary, Lock_Times_Secondary]

K47_name = "K47_Eccentricities"
csv_name = K47_name + ".csv"

#j will verify if the .csv file has already been created
j = 0 #j is 0 when the .csv file does not exist

for item in files:
    if item.find(csv_name) == 0:
        j += 1 # When j is 1, the file exists
        spprint(csv_name + " exist", 2)
        continue

#Reading potentially pre-exsiting data and inserting each column into its own list
if j == 1:
    with open(csv_name, "r") as csvfile:
        K47_csv = csv.reader(csvfile, delimiter = ',')
        #If there was already a pre-exisiting .csv file, we append the data here
        if len(eccentricity) == 0: 
            for row in K47_csv:
                for column in range(len(data)):
                    data[column].append(float(row[column]))

#If the .csv file needs to update data points, it is done here
if len(eccentricity) < len(existing_ecc_folders): 
    #The function below updates data point starting where the .csv was last updated
    #record_data(len(eccentricity), len(existing_ecc_folders), "w")
    for sim in range(len(eccentricity), len(existing_ecc_folders)):
        spprint("Loading simulation: e_0 = " + ecc_range[sim], 1)
        # Load data
        output = vpl.GetOutput(existing_ecc_folders[sim])
        #Extracting the data
        time = output.secondary.Time
        a_crit = output.secondary.CriticalSemiMajorAxis
        lock_time_primary = output.primary.LockTime #Time that primary star tidally locks (Myrs)
        lock_time_secondary = output.secondary.LockTime #Time that secondary star tidally locks (Myrs)
        a_cbp = output.cbp.CBPR #Semi-major axis of the circumbinary planet
        diff_a_crit_a_cbp = a_crit - a_cbp
        #Finding the time in which a_crit = a_cbp
        for t in range(len(time) - 1):
            a1 = diff_a_crit_a_cbp[t]
            t1 = time[t]
            def insert_time(time_value, prefix): #prefix ex: 6 = Myrs, 9 = Gyrs
                conversion = 10**(-prefix)
                return time_a_crit_equals_a_cbp.insert(sim, time_value*conversion)
            if a1 < 0: 
                a2 = diff_a_crit_a_cbp[t + 1]
                t2 = time[t + 1]
                if a2 > 0:
                    #Calculates exactly where at what time a = 0
                    #t_ = (a1*t2 + a2*t1) / (a1 + a2)
                    t_ = (t1*a2 - t2*a1) / (a2 - a1)
                    insert_time(t_, 6) #records time in Myrs
                    print("Inserted time (in Myrs) in which a_crit = a_cbp")
                    break
                elif t2 == time[-1]:
                    #-1 values are used as dummy space and are deleted later before plotting
                    insert_time(-1, 0)
                    print("No time found where a_crit = a_cbp. Inserted -1")
                    break
            
            elif a1 == 0:
                insert_time(t1, 6) #records time in Myrs
                print("Inserted time (in Myrs) in which a_crit = a_cbp")
                break
            
        eccentricity.insert(sim, output.secondary.Eccentricity[0])
        a_crit_minus_a_cbp.insert(sim, max(diff_a_crit_a_cbp))
        print("Inserted max difference between a_crit and a_CBP in AU.")
        
        #For some reason zero becomes a very small negative number in the simulation
        #We convert the tidal-lock array into a scalar
        #The function below considers the last iteration as the tidal-lock time
        def record_lock_time(index, array, new_array):
            #We turn any number less than zero equal to zero with a function
            if array[-1] < 0:
                new_array.insert(index, 0)
            else:
                new_array.insert(index, array[-1]*1e-3) ##Converts from Myrs to Gyrs
            return None

        record_lock_time(sim, lock_time_primary, Lock_Times_Primary)  
        record_lock_time(sim, lock_time_secondary, Lock_Times_Secondary)

        spprint("Inserted Lock time (in Gyrs) of primary and secondary star", 1)
    
    #Now we collect all the data
    rows = zip(eccentricity, 
               a_crit_minus_a_cbp, 
               time_a_crit_equals_a_cbp, 
               Lock_Times_Primary, 
               Lock_Times_Secondary)
    
    #We place all collected data in the .csv file
    with open(csv_name, "w") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
"""
print("Initial Binary Eccentricities")
spprint(eccentricity, 3)
print(r"a_{crit} - a_{cbp}")
spprint(a_crit_minus_a_cbp, 3)

print("Tidal Lock Time: Primary Star")
spprint(Lock_Times_Primary, 3)
print("Tidal Lock Time: Secondary Star")
spprint(Lock_Times_Secondary, 3)
"""
#Making the horizontal data points for panel 2
special_ecc = []

for v in range(len(eccentricity)):
    #Values that are -1 in the list will be removed
    if time_a_crit_equals_a_cbp[0] == -1:
        time_a_crit_equals_a_cbp.pop(0)
    else:
        special_ecc.insert(v, eccentricity[v])
"""
print("length of a_crit = a_cbp:", len(time_a_crit_equals_a_cbp))
print("Time of " + r"a_{crit} = a_{cbp}")
spprint(time_a_crit_equals_a_cbp, 3)
print("length of special Ecc:", len(special_ecc))
print("Special Eccentricity list:")
spprint(special_ecc, 3)
"""

"""
Plotting the maximum difference between a_crit and a_cbp 
(top panel), the time in which maximum was reached (middle
panel), and the tidal lock times for K47A and K47B for all
time during the simulation as a function of initial
binary eccentricity. 
"""

#Defining plot values
lw_plot = 1.1
lw_vline = 1.3*lw_plot
fontsize_axis = 10
labelsize_tick_params = 8
width_tick_params = 0.72
length_tick_params = 2.2


#Color of the simulated data for the top and middle panel
color = vpl.colors.pale_blue
#Defining the overall minimum and maximum tidal lock times to define plotting limits on axes[2] formatting
total_lock_times = Lock_Times_Primary + Lock_Times_Secondary
#Labeling the value of the vertical dashed line
vline = special_ecc[0]

#Eccentrcity in which K47 b begins inside acrit according to Holman & Wiegert's a_crit equation

a_star = 0.080 #AU, always 7.0 days
a_crit = 0.2956 #AU, which is also a_cbp

a_ratio = a_crit/a_star
m1 = 1.043 # Solar masses, mass of primary star
m2 = 0.362 # Solar masses, mass of secondary star
mu = m2/(m1+m2)
c = 1.60 +4.21*mu -5.09*mu**2 - a_ratio
b = 5.1 - 4.27*mu
a = -2.22 + 4.61*mu**2

d = b**2 - 4*a*c # discriminant

if d < 0:
    print("The Holaman & Wiegert equation has no real solution")
elif d == 0:
    x = (-b+np.sqrt(d))/2*a
    print("The Holaman & Wiegert equation has one solutions: ", x)
    if x >= 0 and x < 1:
        e_crit = x
else:
    x1 = (-b+np.sqrt(d))/(2*a)
    x2 = (-b-np.sqrt(d))/(2*a)
    print("The Holaman & Wiegert equation has two solutions: ", x1, " and", x2)
    if x1 >= 0 and x1 < 1:
        e_crit = x1
    if x2 >= 0 and x2 < 1:
        e_crit = x2    
        
e_crit = round(e_crit, 2)
print("e_crit:", e_crit)

#Plotting maximum difference between a_crit and a_cbp over initial binary eccentricity
axes[0].plot(eccentricity, a_crit_minus_a_cbp,
            lw = lw_plot, color = color, ls = "-",
            label = r"$a_{crit} - a_{CBP}$")
axes[0].axhline(0.0, lw = lw_plot, color = "k", ls = "-", 
                label = r"$a_{crit} = a_{CBP}$")
axes[0].axvline(vline, lw = lw_vline, color = "k", 
                ls = "--", label = r"$e_0 = $" + str(vline))

#Format
axes[0].set_ylim(min(a_crit_minus_a_cbp), 
                 max(a_crit_minus_a_cbp))
axes[0].set_ylabel(r"$a_{crit} - a_{CBP}$"
                   + " [AU] ", fontsize = fontsize_axis)
axes[0].legend(loc = "lower right")


#Plotting the time in which the difference between a_crit and a_cbp reached it maximum
axes[1].plot(special_ecc, time_a_crit_equals_a_cbp,
            lw = lw_plot, color = color, ls = "-",
            label = r"$a_{crit} = a_{CBP}$")
axes[1].axvline(vline, lw = lw_vline, color = "k", 
                ls = "--", label = r"$e_0 = $" + str(vline))
axes[1].axvline(e_crit, lw = lw_vline, color = vpl.colors.purple, 
                ls = "--", label = r"$e_{crit} = $" + str(e_crit))

#Format
axes[1].set_ylim(min(time_a_crit_equals_a_cbp), 
                 max(time_a_crit_equals_a_cbp))
axes[1].set_ylabel("Instability Timescale" + " [Myr]", 
                   fontsize = fontsize_axis)
axes[1].legend(loc = (0.4, 0.58))


#Plotting Tidal-lock times of the primary and secondary star
axes[2].plot(eccentricity, Lock_Times_Primary,
            lw = lw_plot, color = vpl.colors.orange, ls = "-",
            label = "K47A")
axes[2].plot(eccentricity, Lock_Times_Secondary,
            lw = lw_plot, color = vpl.colors.red, ls = "-",
            label = "K47B")


#Format
axes[2].set_ylabel("Lock Time [Gyr]", fontsize = fontsize_axis)
axes[2].set_yticks([0.5*i for i in range(9)])
axes[2].set_ylim(min(total_lock_times), 4.0)
axes[2].legend(loc = "upper right")

#Looping some formats that will be the same on all three plots
for n in range(nrows):
    axes[n].set_xlabel("Initial Eccentricity", fontsize = fontsize_axis)
    axes[n].set_xlim(0.1, 0.5)
    axes[n].set_xticks([0.05*i + 0.1 for i in range(9)])
    axes[n].tick_params(axis = 'both', which = 'major', 
                        labelsize = labelsize_tick_params, 
                        width = width_tick_params, 
                        length = length_tick_params)
    axes[n].set_rasterization_zorder(0)

fig.tight_layout()
if (sys.argv[1] == 'pdf'):
    plt.savefig(K47_name + '.pdf', bbox_inches="tight", 
                dpi = 200)
    spprint("Saved figure as a PDF file", 1)
if (sys.argv[1] == 'png'):
    plt.savefig(K47_name + '.png', bbox_inches="tight", 
                dpi = 200)
    spprint("Saved figure as a PNG file", 1)

end_time = datetime.now()
print(end_time)
print('Runtime: {}'.format(end_time - start_time))
