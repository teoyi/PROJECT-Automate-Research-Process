import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import os
import os.path
from scipy.optimize import curve_fit
import shutil

os.getcwd()

# Loading file, and obtaining long name components 
path = "./avgtest"
data_file = os.listdir(path) # Create a list of all files in the folder

files_dict = {} 
files_count = {} 

# Filling up files_dict dictionary to contain list of files names 
for files in data_file: 
    if files[-4:] == '.csv':
        key = files[:-5]
        files_dict.setdefault(key, [])
        files_dict[key].append(files)

# Filling up files_count dictionary to keep track of number of file names with the same parameters
for key, value in files_dict.items(): 
    files_count[key] = len(value)

tb_avg = [] # To be averaged -> file names 
for key, value in files_dict.items(): 
    if len(value) > 1: 
        tb_avg.append([key,len(value)])

# We know it starts A, B, C, D ,E. 5 maximum 
end = ['A.csv', 'B.csv', 'C.csv', 'D.csv', 'E.csv']
    
print("Files that needs to be concatenated (file, count):")
for files in tb_avg:
    print(f'- {files[0]}, {files[1]}')

# Making a new file within the folder that contains all the data
os.chdir(path)
dirName = 'averaged_data'

# Making new directory to put processed data 
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")
    print("Recreating directory...")
    shutil.rmtree(dirName)
    os.mkdir(dirName)

print('Transferring files with count of 1...')
for key, value in files_dict.items(): 
    if len(value) == 1: 
        df = pd.read_csv(value[0])
        df.to_csv(f'./averaged_data/{value[0][:-4]}')

for i in np.arange(0, len(tb_avg)): 
    print(f'Processing {tb_avg[i][0]}')
    file_list = [] 
    for j in np.arange(0, int(tb_avg[i][1])): 
        file_list.append(tb_avg[i][0] + end[j])
    working = pd.concat([pd.read_csv(f) for f in file_list], ignore_index=False, axis = 0)
    working = working.drop(index=0)
    working = working.astype('float64')
    working.to_csv(f'./averaged_data/{file_list[0][:-6]}')
    print('Done!')