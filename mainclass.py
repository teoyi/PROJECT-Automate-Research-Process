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

class Main():
    def __init__(self):
        self.lst = []
        self.params = []
        self.bad_temp = []
        self.bad_offsetn = []
        self.bad_offsetp = []
        self.bad_IT = []
        self.choicefile = []
        self.finalfile = []

    def add_csvs(self):
        while True:
            dir = input("Paste full path to directory here: ")
            if os.path.isdir(dir) == True:
                # Scanning path for files that ends with .csv
                for files in glob.iglob(os.path.join(dir, "*.csv")):
                    #print(files)
                    longname = os.path.basename(files)
                    self.lst.append(longname)
                break
            else:
                print('\n')
                print('Sorry that is not a valid path/directory. Please try again.')
                continue

    def show_csvs(self):
        print('The following files are found in this directory: ')
        print('________________________________________________')
        index = range(len(self.lst))

        for number in index:
            print(str(number + 1) + '. ' + self.lst[number])

    def check_params(self):
        # Splitting longname into their respective parameters
        for files in self.lst:
            split = files.split('_')
            self.params.append(split)
        # if for situations where only 1 file exists
        if len(self.params) == 1:
            self.bad_temp.append(self.params[0][0])
            self.bad_offsetp.append(self.params[0][1])
            self.bad_offsetn.append(self.params[0][2])
            self.bad_IT.append(self.params[0][6])
        else:
            for files in range(len(self.params)-1):
                self.bad_temp.append(self.params[files][0])
                self.bad_offsetp.append(self.params[files][1])
                self.bad_offsetn.append(self.params[files][2])
                self.bad_IT.append(self.params[files][6])

    def file_select(self):
        # Extracting unique values from the list
        exist_t = set(self.bad_temp)
        exist_p = set(self.bad_offsetp)
        exist_n = set(self.bad_offsetn)
        exist_it = set(self.bad_IT)

        # Narrowing down files to be used
        choosing = True
        while choosing:
            while True:
                choicetemp = input('\nWhich temperature?: ')
                if choicetemp in exist_t:
                    break
                else:
                    print('Sorry, data with that temperature does not exist in this directory. Please try again.')
                    continue
            while True:
                choiceoffsetp = input('Which (+) offset?: ')
                if choiceoffsetp in exist_p:
                    break
                else:
                    print('Sorry, data with that (+) offset does not exist. Please try again.')
                    continue
            while True:
                choiceoffsetn = input('Which (-) offset?: ')
                if choiceoffsetn in exist_n:
                    break
                else:
                    print('Sorry, data with that (-) offset does not exist. Please try again.')
                    continue
            while True:
                choiceIT = input('Which integration time?: ')
                if choiceIT in exist_it:
                    break
                else:
                    print('Sorry, data with that integration time does not exist. Please try again.')
                    continue
            break
        #return choicetemp, choiceoffsetp, choiceoffsetn, choiceoffsetp

        for n in range(len(self.params) - 1):
            if (choicetemp == self.params[n][0]
            and choiceoffsetp == self.params[n][1]
            and choiceoffsetn == self.params[n][2]
            and choiceIT == self.params[n][6]):

                self.choicefile.append(self.params[n])

        #print(self.choicefile)

    def selected_files(self):
        for files in range(len(self.choicefile) - 1):
            join = '_'.join(self.choicefile[files])
            self.finalfile.append(join)
        print(self.finalfile)

init = Main()
init.add_csvs()
init.show_csvs()
init.check_params()
init.file_select()
init.selected_files()
