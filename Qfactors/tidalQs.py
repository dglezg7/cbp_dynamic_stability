
# coding: utf-8

# In[ ]:

import subprocess
import sys
import os
import shutil
from datetime import datetime
from random import randrange

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

tidalQ_range = ["1e" + str(4 + i) 
             for i in range(5)] #Stores a range of tidalQs of K47A/B
print(tidalQ_range)

tidalQ_folder_names = ['Q' + Q.replace('.', 'pt') for Q in tidalQ_range]

#Location current directory
directory = os.getcwd()
files = os.listdir(directory) #makes a list of files in your directory

#Creating an empty list to store .in and .wav files
in_files = []

wav_files = []

#The function below collects files of the same type
def collect_files(empty_list, identifier): #identifier must be a string at end of the file
    for file in range(len(files)):
        if files[file].endswith(identifier): #chooses files ending with .in
            empty_list.insert(file, files[file]) #Inserts chosen files to data list
        
collect_files(in_files, ".in") #Makes a list of all .in files
collect_files(wav_files, ".wav") #Makes a list of all .wav audio files

"""
If running the script starting from the middle of an iteration,
the leftover .forward and .log files from the unfinished simulation 
will be deleted in order to avoid any mixture of new files.
"""

#Creating an empty list to collect unfinished .forward and .log files
incomplete_data = []
collect_files(incomplete_data, ".forward")
collect_files(incomplete_data, ".log")

#Deleting every file inside the incomplete_data list
if len(incomplete_data) > 0:
    for garbage in incomplete_data:
        os.remove(garbage)
    files = os.listdir(directory) #Refreshing list of files in your directory


#Defining function that'll reaplace target strings of the .in files
#This function changes the system name and initial conditions in the .in files to the next iteration
def next_iteration(iteration, lines):
    #Iterating through each line of file
    for index in range(len(lines)):
        #Identifying line with outputs the name on the .forward files
        if lines[index].find("sOutFile") == 0 or lines[index].find("sSystemName") == 0:
            lines[index] = lines[index].replace(tidalQ_folder_names[iteration], 
                                                tidalQ_folder_names[iteration + 1])
            print("changed system name of " + in_files[dot_in_file]
                 + " from K47_" + tidalQ_folder_names[iteration] + " to K47_"
                 + tidalQ_folder_names[iteration + 1])
            print("New line: " + lines[index])
        #Identifying line with the tidalQ (In primary.in and secondary.in)
        if lines[index].find("dTidalQ") == 0:
            print(lines[index])
            lines[index] = lines[index].replace(tidalQ_range[iteration], 
                                                tidalQ_range[iteration + 1])
            print("changed tidalQ in .in from K47_"
                 + tidalQ_range[iteration] + " to K47_"
                 + tidalQ_range[iteration + 1])
            print("New line: " + lines[index])
            continue  

        
print("------------------------------------------------------------------------\n"
      "NOTE: In order to save print space, 'secondary.in' will only be printed.\n"
      "If you want to check the other files, they'll all be stored in each of\n"
      "their own respected folder." 
      "------------------------------------------------------------------------\n")

f = open("secondary.in", 'r') #Reads the file
print(f.read()) #Prints the whole file
f.close() #Closes the file


###############################################################
###############################################################

        
#Iterate through the tidalQs
for tidalQ in range(len(tidalQ_range)):
    spprint("Simulation: tidalQ = " + tidalQ_range[tidalQ], 2)
    #Keeps track of potentially pre-existing simulations
    existing_tidalQ_folders = []
    #Iterates through all files and folders in "files"
    for item in range(len(files)):
        #If statement below identifies potentially pre-exisiting simulated folder
        if files[item].find("e0pt") == 0:
            existing_tidalQ_folders.insert(len(existing_tidalQ_folders), files[item])
    for folder in range(len(existing_tidalQ_folders) + 1):
        if len(existing_tidalQ_folders) < tidalQ + 1:
            #Running simulation, which produces .forward and .log files
            subprocess.call(["vplanet", "vpl.in"])
            spprint("SIMULATION COMPLETE", 1)
            #Plays "Simulation Complete" audio in Polish... lol
            if len(wav_files) > 0:
                #You can comment/uncomment either of these q values, just leave one on.
                #For random order 
                q = randrange(len(wav_files))
                #For a repetitive sequence
                #q = ecc % len(wav_files)
                #Line below plays the audio file
                os.system("aplay " + wav_files[q])
            
            #Creating folder for the simulation
            os.mkdir(str(tidalQ_folder_names[tidalQ]))
            spprint("Created new directory " + str(tidalQ_folder_names[tidalQ]), 1)
            
            #Stores the simulated data
            data = []
            
            #reupdating list of files in order to show the new simulated files
            files = os.listdir(directory) 

            #Collecting .forward and .log files into one list
            collect_files(data, ".forward")
            collect_files(data, ".log")
            print(data)
            
            #Destination of folder where simulations will be transported
            destination = tidalQ_folder_names[tidalQ] 

            for file in data: 
                #Moves files to destined folder
                shutil.move(os.path.join(directory, file),
                            os.path.join(destination, file))
                print("cut and pasted " + file + " from ")
                print(str(directory) + " to ") 
                spprint(str(directory + destination), 1)
                
            for file in in_files: 
                #Copies and pastes .in files to destined folder
                shutil.copyfile(os.path.join(directory, file),
                                os.path.join(destination, file))
                print("copied and pasted " + file + " from ")
                print(str(directory) + " to ") 
                spprint(str(directory + destination), 1)
            break
        else:
            spprint("Simulation already exists.", 2)
            break
    
    #Calling all .in files in order to change the tidalQ and system name
    for dot_in_file in range(len(in_files)):
        spprint("reading file " + in_files[dot_in_file], 2)
        #Places each line of file into its own 
        lines_of_file = open(in_files[dot_in_file]).read().splitlines()
        
        #Replacing target strings
        if tidalQ < len(tidalQ_range) - 1:
            #Iterating through each line of file
            next_iteration(tidalQ, lines_of_file)
        else:
            #After last simulation, original settings are set back
            next_iteration(-1, lines_of_file)
        
        #Overwriting file and saving it
        open(in_files[dot_in_file], 'w').write('\n'.join(lines_of_file))
        spprint("overwriting file " + in_files[dot_in_file], 1)
    
    f = open("primary.in", 'r') #Reads the file
    print(f.read()) #Prints the whole file
    f.close() #Closes the file
    
end_time = datetime.now()
print(end_time)
print('Runtime: {}'.format(end_time - start_time))
