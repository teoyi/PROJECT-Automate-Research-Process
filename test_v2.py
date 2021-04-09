# Data Science Import
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
# OS manipulation import 
import os
import os.path
import shutil


'''
First section contains file manipulation to take into account of multiple runs of the experiment 
'''
print(f"Working from {os.getcwd()}")

# Loading file, and obtaining long name components 
path1 = "./avgtest"
data_file = os.listdir(path1) # Create a list of all files in the folder

files_dict = {} 
# Filling up files_dict dictionary to contain list of files names 
for files in data_file: 
    if files[-4:] == '.csv':
        key = files[:-5]
        files_dict.setdefault(key, [])
        files_dict[key].append(files)

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
os.chdir(path1)
dirName = 'final_data'

# Making new directory to put processed data 
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("\nDirectory " , dirName ,  " Created ")
else:    
    print("\nDirectory " , dirName ,  " already exists")
    print("Recreating directory...")
    shutil.rmtree(dirName)
    os.mkdir(dirName)

print('\nTransferring files with count of 1...')
for key, value in files_dict.items(): 
    if len(value) == 1: 
        dummy1 = pd.read_csv(value[0])
        dummy1.to_csv(f'./{dirName}/{value[0][:-4]}')
print('Done!')

for i in np.arange(0, len(tb_avg)): 
    print(f'\nProcessing {tb_avg[i][0]}')
    file_list = [] 
    for j in np.arange(0, int(tb_avg[i][1])): 
        file_list.append(tb_avg[i][0] + end[j])
    working = pd.concat([pd.read_csv(f) for f in file_list], ignore_index=False, axis = 0)
    working = working.drop(index=0)
    working = working.astype('float64')
    working.to_csv(f'./{dirName}/{file_list[0][:-6]}', index= False)
    print('Done!')

# Final check of data quality and structure 
print('\n*** Checking processed data integrity ***')
path_check = f'./{dirName}'
check_list = os.listdir(path_check)
check_str1 = "Index(['Unnamed: 0', 'Wavelength', 'S2c', 'Wavelength.1', 'S2'], dtype='object')"
check_str2 = "Index(['Wavelength', 'S2c', 'Wavelength.1', 'S2'], dtype='object')"
for files in check_list: 
    dummy2 = pd.read_csv(path_check + f'/{files}')
    if str(dummy2.columns) == check_str1 or str(dummy2.columns) == check_str2:
        pass
    else:
        os.remove(path_check+f'/{files}')
        print(f'\n{files} has been removed for not having the correct structure/format.')


'''
Second section deals with the curve fitting processes 
'''
# Loading file, and obtaining long name components 
path2 = f"./{dirName}"
data_list = os.listdir(path2) 

# Empty list will be appended with the respective inputs in the order they are listed in the folder 
volts = [] # Empty list to store input voltage values 
c_temp = [] # Empty list to store calculated carrier temperature values 

# Making new directory to put plots created
print(os.getcwd())
dirName2 = 'processed_plot'
if not os.path.exists(path2+'/'+dirName2):
    os.mkdir(path2+'/'+dirName2)
    print("\nDirectory " , dirName2 ,  " Created ")
else:    
    print("\nDirectory " , dirName2 ,  " already exists")
    print("Recreating directory...")
    shutil.rmtree(path2+'/'+dirName2)
    os.mkdir(path2+'/'+dirName2)

# Constants to be used 
h = 4.1357 * 10 ** -15 # Plancks constant in eV*s
c = 2.99792458 * 10 ** 8 # Speed of light in m/s 
k = 8.617333262145 * 10 ** -5 # Boltzmann constant in eV/K
comp = 0.939162 # Composition for InGaAs, estimated by Peter, solved through Wolfram Alpha 

# Creating curve fit function 
def guess_check(title_str, xdata, ydata, label1, label2, plot_title, bandE): 
    # Curve fit function: 
    def first_pass(E, b, c): 
        return c  * E * np.sqrt(E-bandE) * np.exp(-E*b) # bandE and k are already defined previously 

    def second_pass(E, a, b, c): 
        return a + c  * E * np.sqrt(E-bandE) * np.exp(-E*b) 

    # Curve fit range and weight:
    E = np.linspace(np.min(xdata), np.max(xdata), len(xdata))
    weight_func = np.exp(E*6)

    popt1, pcov1 = curve_fit(first_pass, xdata, ydata, maxfev = 10000, sigma = weight_func, absolute_sigma=True) 
    #print(popt1)
    p0_b = popt1[0]
    p0_c = popt1[1]

    popt2, pcov2 = curve_fit(second_pass, xdata, ydata, maxfev = 10000, p0 = [0,p0_b,p0_c], sigma=weight_func, absolute_sigma=True)
    #print(popt2)
    pfinal_a = popt2[0]
    pfinal_b = popt2[1]
    pfinal_c = popt2[2] 

    print(f''' 
{title_str}
_____________________________________________

Initial Guess Parameters: 
    b = {popt1[0]}
    c = {popt1[1]}

Final Fit Parameters: 
    a = {popt2[0]}
    b = {popt2[1]}
    c = {popt2[2]}
    ''')

    fig = plt.figure()
    plt.plot(xdata, ydata, 'o', label=label1)
    plt.plot(xdata, second_pass(xdata, *popt2), '-', label=label2)
    plt.ylabel('Emission Intensity (a.u.)')
    plt.xlabel('Photon Energy (eV)')
    plt.yscale('log')
    plt.title(plot_title)
    plt.legend()
    plt.ioff()
    plt.savefig(path2 + f"/{dirName2}/{plot_title}")
    plt.close(fig)
    return p0_b, p0_c, pfinal_a, pfinal_b, pfinal_c, fig

# Beginning Script 
for files in data_list: 
    if (files == ".DS_Store"): 
        pass 
    else: 
        print(f'\nCurrently Processing: {files}')
        # Reading .csv files 
        test_df = pd.read_csv(path2+f"/{files}")
        col = test_df.columns

        components = files.split("_")
        volts.append(components[1]) # Append input voltage
        latticeT = float(components[0]) + 273.15 # Reading from long name 
        bandE = 0.42+0.625*comp*(5.8/(latticeT+300)-4.19/(latticeT+271))*10**-4 * latticeT**2 * comp - (4.19*10**-4 * latticeT**2)/(latticeT+271) + 0.475*comp**2 # in eV, bandgap energy for InGaAs. 

        # Creating new df to not mess with original 
        if len(col) == 4: 
            new_df = pd.DataFrame() 
            new_df[col[0]] = test_df[col[0]].iloc[1:] # Wavelength, using iloc to remove non numerical value 
            new_df[col[1]] = test_df[col[1]].iloc[1:] # S2c 
            new_df[col[3]] = test_df[col[3]].iloc[1:] # S2
            new_df = new_df.astype(float) # Converting data values to numeric from strings, prep for parse in plot
            
            # Creating additional columns to be used for further calculations 
            new_df['Photon Energy'] = (h*c)/(new_df[col[0]]*10**-9)
            new_df['Multiplier'] = new_df['S2c']/new_df['S2']

            # dLambda conversion to dE 
            scale = 1240
            new_df['dE_Conv S2c'] =  new_df[col[1]] * new_df[col[0]] / scale
            new_df['dE_Conv S2'] = new_df[col[3]] * new_df[col[0]] / scale

        elif len(col) == 5: 
            new_df = pd.DataFrame() 
            new_df[col[1]] = test_df[col[1]].iloc[1:] # Wavelength, using iloc to remove non numerical value 
            new_df[col[2]] = test_df[col[2]].iloc[1:] # S2c 
            new_df[col[4]] = test_df[col[4]].iloc[1:] # S2
            new_df = new_df.astype(float) # Converting data values to numeric from strings, prep for parse in plot

            # Creating additional columns to be used for further calculations 
            new_df['Photon Energy'] = (h*c)/(new_df[col[1]]*10**-9)
            new_df['Multiplier'] = new_df['S2c']/new_df['S2']

            # dLambda conversion to dE 
            scale = 1240
            new_df['dE_Conv S2c'] =  new_df[col[2]] * new_df[col[1]] / scale
            new_df['dE_Conv S2'] = new_df[col[4]] * new_df[col[1]] / scale

        # Applying curve fit function 
        # DC-offset Correction 
        dc_guessb, dc_guessc, dc_fita, dc_fitb, dc_fitc, fig = guess_check('DC-Offset Calculations', new_df['Photon Energy'], new_df['S2c'], 'S2c', 'S2c fit', components[0] + '_' + components[1] + '_' +'DC-Offset Fit', bandE)
        # Since dLambda to dE correction is already done with another column, we can skip straight to multiplier correction 

        # Multiplier Correction 
        new_df['Corrected S2'] = (new_df['dE_Conv S2'] - dc_fita) * new_df['Multiplier']
        guessb, guessc, final_a, final_b, final_c, fig = guess_check('Final Fit Calculation', new_df['Photon Energy'], new_df['Corrected S2'], 'Corrected S2', 'Corrected fit', components[0] + '_' + components[1] + '_' +'final fit', bandE)
        e_temp = 1/(k*final_b)
        print(f"The carrier temperature is {e_temp} K.")
