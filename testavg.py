import pandas as pd
import numpy as np
import glob
import os

dir = "/Users/luke/Desktop/Python/GitClone/PROJECT-Automate-Research-Process/testfolder"

files = os.listdir(dir)
files_of_interests = {}

for filename in files:
    if filename[-4:] == '.csv':
        key = filename[:-5]
        files_of_interests.setdefault(key, [])
        files_of_interests[key].append(filename)
        print(filename)

print(files_of_interests)
print(os.path.join(dir, filename))
#wavelength_r = np.arange(1100, 1500, 10)
# wl_df = pd.DataFrame.from_records([wavelength_r]).T
# print(wl_df)
# for key in files_of_interests:
#     #stack_df = pd.DataFrame.from_records([wavelength_r]).T
#     #stack_df = stack_df.rename(columns = {'1', 'Wavelength'})
#     stack_df = pd.DataFrame()
#     print(stack_df)
#     for filename in files_of_interests[key]:
#         stack_df = stack_df.append(pd.read_csv(os.path.join(dir, filename)))
#         #stack_df.set_index('Unnamed:0', inplace = True)
    # print(stack_df)
# dflist = []
# for key in files_of_interests:
#     for filename in files_of_interests[key]:
#         dflist.append(pd.read_csv(os.path.join(dir, filename)) )
# concat = pd.concat(dflist, axis = 1)
# concat.to_csv(dir + '/concat.csv')
# ``\

#df = (pd.read_csv(os.path.join(dir, filename)) for key in files_of_interests for filename in key)
#df = pd.concat([pd.read_csv(os.path.join(dir, filename))
                #for key in files_of_interests for filename in files_of_interests[key]], axis = 1)

#df = df.groupby(['Unnamed: 0', 'Wavelength', 'Wavelength.1']).mean().reset_index()

for key in files_of_interests:
    list = []
    for filename in files_of_interests[key]:
        list.append(pd.read_csv(os.path.join(dir,filename)))
        df = pd.concat(list, axis = 1)
        df = df.drop(['Unnamed: 0', 'Wavelength.1'], axis = 1)
        df = df.groupby(['Wavelength']).mean().reset_index(inplace = True)
        print(df)
        #df.to_csv(os.path.join(dir + '/', f"{filename[:-5]}_master.csv"))
