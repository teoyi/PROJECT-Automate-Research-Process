# Data Science Import
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import cmath
# OS manipulation import 
import os
import os.path
import shutil

'''
**** SECTION 1 ****
This section contains mathematical functions to calculate values to be used.
1. Composition Solver 
2. Curve fit function 
'''
def comp_solver(rt_band):
    '''
    Used to solve a quadratic equation to determine composition of semiconductor material.
    Quadratic equation is taken from http://www.ioffe.ru/SVA/NSM/Semicond/GaInAs/bandstr.html by Paul.
    The quadratic equation is of the form: 
        - quad_eqn  = 0.475*x**2 + (0.625*(5.8/(latticeT+300)-4.19/(latticeT+271))*10**-4 * latticeT**2)*x + (0.42 - (4.19*10**-4 * latticeT**2)/(latticeT+271) - rt_band) 

    **Note**: This requires users to import cmath (complex math library)

    :param float rt_band: Bandgap energy at ambient temperature (assumed at 298K). 
    :rtype: float 
    '''
    a = 0.475
    b = (0.625*(5.8/(298+300)-4.19/(298+271))*10**-4 * 298**2)
    c = (0.42 - (4.19*10**-4 * 298**2)/(298+271) - rt_band) 

    # calculating  the discriminant
    dis = (b**2) - (4*a*c)
    
    # find two results
    ans1 = (-b - cmath.sqrt(dis))/(2 * a)
    ans2 = (-b + cmath.sqrt(dis))/(2 * a)
    
    if (ans1.real < 0): 
        print(f"The composition is: {ans2.real}.")
        return ans2.real 
    else: 
        print(f"The composition is: {ans1.real}.")
        return ans1.real 

def guess_check(xdata, ydata, label1, label2, plot_title, bandE): 
    '''
    Used to automate the process of feeding guesses twice to solve for the best fit variable.
    Plots are also automatically made and saved to a pre-created directory: "processed_plots" 

    :param numpy arr xdata: X axis data read from .csv files or user created data frame 
    :param numpy arr ydata: Y axis data read from .csv files or user created data frame 
    :param str label1: Label for markers of original data 
    :param str label2: Label for markers of fitted data 
    :param str plot_title: User input for the plot's title
    :param float bandE: Calculated bandgap energy the specific temperature 
    :rtype: float  
    '''
    # Curve fit function: 
    def first_pass(E, b, c): 
        return c  * E * np.sqrt(E-bandE) * np.exp(-E*b) # bandE and k are already defined previously 

    def second_pass(E, a, b, c): 
        return a + c  * E * np.sqrt(E-bandE) * np.exp(-E*b) 


    # Curve fit range and weight:
    E = np.linspace(np.min(xdata), np.max(xdata), len(xdata))
    weight_func = np.exp(-E*12)

    popt1, pcov1 = curve_fit(first_pass, xdata, ydata, maxfev = 10000, sigma = weight_func, absolute_sigma=True) 
    #print(popt1)
    p0_b = popt1[0]
    p0_c = popt1[1]

    popt2, pcov2 = curve_fit(second_pass, xdata, ydata, maxfev = 10000, p0 = [0,p0_b,p0_c], sigma=weight_func, absolute_sigma=True)
    #print(popt2)
    pfinal_a = popt2[0]
    pfinal_b = popt2[1]
    pfinal_c = popt2[2] 

    fig = plt.figure()
    plt.plot(xdata, ydata, 'o', label=label1, color='black')
    plt.plot(xdata, second_pass(xdata, *popt2), '-', label=label2, color='red')
    plt.ylabel('Emission Intensity (a.u.)')
    plt.xlabel('Photon Energy (eV)')
    # plt.yscale('log')
    plt.title(plot_title)
    plt.legend(frameon=False)
    plt.ioff()
    plt.savefig(path2 + f"/{dirName2}/{plot_title}.png", bbox_inches='tight')
    plt.close(fig)
    return p0_b, p0_c, pfinal_a, pfinal_b, pfinal_c, fig

'''
**** SECTION 2 ****
This section contains script for file manipulation. 
File manipulation includes: 
    - Reading files
    - Creating/Removing directories
    - Editing .csv file contents 
    - Check of processed file structure and integrity 
    - Saving final file contents to new directory  
'''
print(f"Working from {os.getcwd()}")

# Loading file, and obtaining long name components 
path1 = "./updated_test/843"
splitted = path1.split('/')
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

# Multiple runs contains end letters of A, B, C, D ,E. 5 maximum 
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
    print("\nDirectory **" , dirName ,  "** Created ")
else:    
    print("\nDirectory **" , dirName ,  "** already exists")
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
response = input('Do you want to process files with integration time = 1s? (y/n): ').lower()

if (response == 'y'):
    print("Files with integration time of 1 will be kept.")
    for files in check_list: 
        dummy2 = pd.read_csv(path_check + f'/{files}')
        if str(dummy2.columns) == check_str1 or str(dummy2.columns) == check_str2:
            pass
        else:
            os.remove(path_check+f'/{files}')
            print(f'\n{files} has been removed for not having the correct structure/format.')
else: 
    print("Files with integration time of 1 will be removed.")
    for files in check_list: 
        if files[-1] == '1':
            os.remove(path_check+f'/{files}')
            print(f'\n{files} has been removed for having integration time of 1.')
        else: 
            dummy2 = pd.read_csv(path_check + f'/{files}')
            if str(dummy2.columns) == check_str1 or str(dummy2.columns) == check_str2:
                pass
            else:
                os.remove(path_check+f'/{files}')
                print(f'\n{files} has been removed for not having the correct structure/format.')

# Loading new file, and obtaining long name components 
path2 = f"./{dirName}"
data_list = os.listdir(path2) 

# Making new directory to put plots created
dirName2 = 'processed_plot'
if not os.path.exists(path2+'/'+dirName2):
    os.mkdir(path2+'/'+dirName2)
    print("\nDirectory **" , dirName2 ,  "** Created ")
else:    
    print("\nDirectory **" , dirName2 ,  "** already exists")
    print("Recreating directory...")
    shutil.rmtree(path2+'/'+dirName2)
    os.mkdir(path2+'/'+dirName2)

'''
**** SECTION 3 ****
This section will contains the script to process data to return carrier temperature. 
Plot of carrier temperature against input voltage will be made and saved into the same folder, "processed_plot"
'''
# Using user input to calculate for composition 
rt_band = float(input("Eg at room temp: "))

# Constants to be used 
h = 4.1357 * 10 ** -15 # Plancks constant in eV*s
c = 2.99792458 * 10 ** 8 # Speed of light in m/s 
k = 8.617333262145 * 10 ** -5 # Boltzmann constant in eV/K
comp = comp_solver(rt_band) # Composition for InGaAs 

# Empty list will be appended with the respective inputs in the order they are listed in the folder 
volts = [] # Store input voltage values 
c_temp = [] # Store calculated carrier temperature values 
o_temp = [] # Store lattice temp from long name  

# Beginning Script 
for files in data_list: 
    if (files == ".DS_Store"): 
        pass 
    else: 
        #print(f'\nCurrently Processing: {files}')
        # Reading .csv files 
        test_df = pd.read_csv(path2+f"/{files}")
        col = test_df.columns

        components = files.split("_")
        o_temp.append(components[0])
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

        new_df = new_df.sort_values('Wavelength') # Sorting x values to prevent straight lines
        # Applying curve fit function 
        # DC-offset Correction 
        dc_guessb, dc_guessc, dc_fita, dc_fitb, dc_fitc, fig = guess_check(new_df['Photon Energy'], new_df['S2c'], 'S2c', 'S2c fit', components[0] + '_' + components[1] + '_' +'DC-Offset Fit', bandE)
        # Since dLambda to dE correction is already done with another column, we can skip straight to multiplier correction 

        
        # Multiplier Correction 
        new_df['Corrected S2'] = (new_df['dE_Conv S2'] - dc_fita) * new_df['Multiplier']
        guessb, guessc, final_a, final_b, final_c, fig = guess_check(new_df['Photon Energy'], new_df['Corrected S2'], 'Corrected S2', 'Corrected fit', components[0] + '_' + components[1] + '_' +'final fit', bandE)
        e_temp = 1/(k*final_b)
        c_temp.append(e_temp)
        print(f"\nFor {files} the carrier temperature is {e_temp} K.")
        # print(f"The carrier temperature is {e_temp} K.")

# Checking final data to be plotted for carrier temp plot 
for i in np.arange(0, len(volts)):
    if volts[i][0] == 'p':
        volts[i] = volts[i][1:]
    elif volts[i][0] == 'n': 
        volts[i] = '-' + volts[i][1:]
print(volts)
volt_int = list(map(float, volts))
otemp_int = list(map(float, o_temp))
for i in np.arange(0, len(c_temp)):
    c_temp[i] = c_temp[i]-273.15

print(c_temp)
avg_temp = sum(c_temp)/len(c_temp)
latt_temp = int(sum(otemp_int)/len(otemp_int))
new_x, new_y = zip(*sorted(zip(volt_int, c_temp)))
# print(new_x)
# print(new_y)
fig = plt.figure()
if (splitted[-1] == '995'):
    plt.scatter(new_x, new_y, color='black', marker='s', label='Carrier Temperature')
    plt.axhline(latt_temp, ls='--', color='black', label=f'Lattice Temperature')
    plt.text(15, latt_temp+4, f'{latt_temp}')
    plt.axhline(avg_temp, ls='--', color='red', label=f'Avg. Carrier Temperature')
    plt.text(15, avg_temp+4, f'{int(avg_temp)}', color='red')
    plt.ylabel('Carrier Temperature ($^\circ$C)')
    plt.xlabel('Voltage (mV)')
    plt.legend(frameon=False, prop={'size': 8})
    plt.ioff()
    plt.savefig(path2 + f"/{dirName2}/c_temp.png", bbox_inches='tight')
    plt.close(fig)
elif (splitted[-1] == '843'):
    plt.scatter(new_x, new_y, color='black', marker='s', label='Carrier Temperature')
    plt.axhline(latt_temp, ls='--', color='black', label=f'Lattice Temperature')
    plt.text(255, latt_temp+7, f'{latt_temp}')
    plt.axhline(avg_temp, ls='--', color='red', label=f'Avg. Carrier Temperature')
    plt.text(255, avg_temp+7, f'{int(avg_temp)}', color='red')
    plt.ylabel('Carrier Temperature ($^\circ$C)')
    plt.xlabel('Voltage (mV)')
    plt.legend(frameon=False)
    plt.ioff()
    plt.savefig(path2 + f"/{dirName2}/c_temp.png", bbox_inches='tight')
    plt.close(fig)
