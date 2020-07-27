'''
PROJECT: Research Process Automation for Ufe Lab

Objective of this program:

1. Recognize longname of the files
2. Process Multiple csv file of the same category/params to get desired values
3. Transfer new values to a new csv file for viewing
4. Be able to plot the graphs and view it as needed
5. Potentially a GUI to host all commands there

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob # For listing out files in a directory
import os


# Extracting full name of .csv files since there is a format to it
lst = []
while True:
    dir = input("Paste full path to directory here: ")
    if os.path.isdir(dir) == True:
        for files in glob.iglob(os.path.join(dir, "*.csv")): # Creates an interable of all .csv files
            longname = os.path.basename(files)
            lst.append(longname) # Place file names into a list
        break

    else:
        print('\n')
        print('Sorry that is not a valid path/ not a directory. Please try again.')
        continue

print('\n')
print('The following files are found in this directory: ')
for files in lst:
    print('\t' + files)

# Dissecting the longname through sep = '_'
params = []
for file in lst:
    split = file.split('_')
    params.append(split)

# Narrowing down the files to what you want to use
choicetemp = input('Which temperature?: ')
choiceoffsetp = input('Which (+) offset?: ')
choiceoffsetn = input('Which (-) offset?: ')
choiceIT = input('Which integration time?: ')

choicefile = []
for n in range(len(params)-1):
    # print(params[n])
    if choicetemp == params[n][0] and choiceoffsetp == params[n][1] and choiceoffsetn == params[n][2] and choiceIT == params[n][6]:
        choicefile.append(params[n])
    else:
       pass


# Converting it back to longname format, to be opened and manipulated
finalfile = []
for files in range(len(choicefile)-1):
    join = '_'.join(choicefile[files])
    finalfile.append(join)

print(finalfile)
