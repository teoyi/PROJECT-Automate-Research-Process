import pandas as pd
import numpy as np
import glob
import os

dir = "/Users/luke/Desktop/testfolder"

files = os.listdir(dir)
files_of_interests = {}

for filename in files:
    if filename[-4:] == '.csv':
        key = filename[:-4]
        files_of_interests.setdefault(key, [])
        files_of_interests[key].append(filename)

print(files_of_interests)

wavelength_r = np.arange(1100, 1500, 10)
# wl_df = pd.DataFrame.from_records([wavelength_r]).T
# print(wl_df)
for key in files_of_interests:
    stack_df = pd.DataFrame.from_records([wavelength_r]).T
    print(stack_df)
    for filename in files_of_interests[key]:
        stack_df = stack_df.append(pd.read_csv(dir + '/' + filename, usecols = ["S2c", "S2"]))
    print(stack_df)
