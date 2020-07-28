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

def get_choice():
    # Extracting full name of .csv files since there is a format to it
    lst = []
    while True:
        dir = input("Paste full path to directory here: ")
        if os.path.isdir(dir) == True:
            for files in glob.iglob(os.path.join(dir, "*.csv")): # Creates an interable of all .csv files
                longname = os.path.basename(files)
                lst.append(longname) # Place file names into a list
            return lst
            break

        else:
            print('\n')
            print('Sorry that is not a valid path/ not a directory. Please try again.')
            continue

    #print(lst)
    print('\n')
    print('The following files are found in this directory: ')
    for files in lst:
        print('\t' + files)

    # Dissecting the longname through sep = '_'
    params = []
    for file in lst:
        split = file.split('_')
        params.append(split)
    return params
    #print(len(params))

    # Creating a list of existing parameter
    bad_temp = []
    bad_offsetp = []
    bad_offsetn = []
    bad_IT = []

    if len(params) == 1:
        exist_t = bad_temp.append(params[0][0])
        exist_op = bad_offsetp.append(params[0][1])
        exist_on = bad_offsetn.append(params[0][2])
        exist_IT = bad_IT.append(params[0][6])
    else:
        for files in range(len(params)-1):
            exist_t = bad_temp.append(params[files][0])
            exist_op = bad_offsetp.append(params[files][1])
            exist_on = bad_offsetn.append(params[files][2])
            exist_IT = bad_IT.append(params[files][6])
        return bad_temp, bad_offsetn, bad_offsetp, bad_IT

    #print(bad_temp)
    temp_exist = set(bad_temp)
    offsetp_exist = set(bad_offsetp)
    offsetn_exist = set(bad_offsetn)
    IT_exist = set(bad_IT)
    print(temp_exist)

    choosing = True
    while choosing:
        # Narrowing down the files to what you want to use
        while True:
            choicetemp = input('Which temperature?: ')
            if choicetemp in temp_exist:
                break
            else:
                print('Sorry, data with that temperature does not exist in this directory. Please try again.')
                continue
        while True:
            choiceoffsetp = input('Which (+) offset?: ')
            if choiceoffsetp in offsetp_exist:
                break
            else:
                print('Sorry, data with that (+) offset does not exist. Please try again.')
                continue
        while True:
            choiceoffsetn = input('Which (-) offset?: ')
            if choiceoffsetn in offsetn_exist:
                break
            else:
                print('Sorry, data with that (-) offset does not exist. Please try again.')
                continue
        while True:
            choiceIT = input('Which integration time?: ')
            if choiceIT in IT_exist:
                break
            else:
                print('Sorry, data with that integration time does not exist. Please try again.')
                continue
        break

    choicefile = []
    for n in range(len(params)-1):
        # print(params[n])
        if choicetemp == params[n][0] and choiceoffsetp == params[n][1] and choiceoffsetn == params[n][2] and choiceIT == params[n][6]:
            choicefile.append(params[n])
    return choicefile
    #print(choicefile)

    # Converting it back to longname format, to be opened and manipulated
    finalfile = []
    for files in range(len(choicefile)-1):
        join = '_'.join(choicefile[files])
        finalfile.append(join)
    return finalfile
    #print(finalfile)

finalfile = get_choice()
print(finalfile[1])


def openfile(finalfile,dir):
    for files in range(len(finalfile)-1):
        df = pd.read_csv(finalfile[files])
        # Correcting for bug
        if df["S2"] > 10000:
            print(df["S2"])
        else:
            pass

# get_choice()
openfile(get_choice())
