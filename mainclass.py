'''
PROJECT: Research Process Automation for Ufe Lab
Objective of this program:
1. Recognize longname of the files
2. Process Multiple csv file of the same category/params to get desired values
3. Transfer new values to a new csv file for viewing
4. Be able to plot the graphs and view it as needed
5. Potentially a GUI to host all commands there
'''
###############################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob # For listing out files in a directory
import os
###############################################################################

class Initial():
    def __init__(self):
        self.lst = []
        self.params = []
        self.bad_temp = []
        self.bad_offsetn = []
        self.bad_offsetp = []
        self.bad_IT = []
        self.choicefile = []
        self.finalfile = []


    def get_path(self):
        while True:
            dir = input("Paste full path to directory here: ")
            if os.path.isdir(dir) == True:
                for files in glob.iglob(os.path.join(dir, "*.csv")):
                    print(files)
                    longname = os.path.basename(files)
                    self.lst.append(longname)
                return self.lst
                break
            else:
                print('\n')
                print('Sorry that is not a valid path/directory. Please try again.')
                continue

# init = Initial()
# init.get_path()
dir = input("Paste full path to directory here: ")
#print(dir)
# onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
# print(onlyfiles)
if os.path.isdir(dir) == True:
    onlyfiles = glob.iglob(os.path.join(dir,".csv"))
    for files in onlyfiles:
        print(files)

print(list(onlyfiles))
# print(init.lst)
print('\n')
print('The following files are found in this directory: ')
# for files in init.lst:
#     print('\t' + files)
