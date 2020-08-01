import pandas as pd
import numpy as np
import glob
import os

dir = "/Users/luke/Desktop/testfolder"

files = os.listdir(dir)
files_of_interests = {}

for filename in files:
    if filename[-4:] == '.csv':
        key = filename[:-5]
        files_of_interests.setdefault(key, [])
        files_of_interests[key].append(filename)

print(files_of_interests)

#wavelength_r = np.arange(1100, 1500, 10)
# wl_df = pd.DataFrame.from_records([wavelength_r]).T
# print(wl_df)
for key in files_of_interests:
    #stack_df = pd.DataFrame.from_records([wavelength_r]).T
    #stack_df = stack_df.rename(columns = {'1', 'Wavelength'})
    stack_df = pd.DataFrame()
    print(stack_df)
    for filename in files_of_interests[key]:
        stack_df = stack_df.append(pd.read_csv(os.path.join(dir, filename)))
        #stack_df.set_index('Unnamed:0', inplace = True)
    print(stack_df)
