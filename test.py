import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import os
import os.path
from scipy.optimize import curve_fit

# Loading file, and obtaining long name components 
path = "./testfolder2"
data_list = os.listdir(path) # Create a list of all files in the folder
#print(data_list)

# Empty list will be appended with the respective inputs in the order they are listed in the folder 
volts = [] # Empty list to store input voltage values 
c_temp = [] # Empty list to store calculated carrier temperature values 

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
    plt.show()
    return p0_b, p0_c, pfinal_a, pfinal_b, pfinal_c, fig

# Beginning Script 
# looping = True
# while looping: 
for files in data_list: 
    if (files == ".DS_Store" or files != data_list[3]): 
        pass 
    else: 
        print(f'Currently Processing: {files}')
        
        # Reading .csv files 
        test_df = pd.read_csv(path+f"/{files}")
        col = test_df.columns
        # if (len(col) != 4):
        #     print(f'{files} does not have the correct columns')
        #     print(col)
        # else: 
        components = files.split("_")
        volts.append(components[1]) # Append input voltage
        latticeT = float(components[0]) # Reading from long name 
        bandE = 0.42+0.625*comp*(5.8/(latticeT+300)-4.19/(latticeT+271))*10**-4 * latticeT**2 * comp - (4.19*10**-4 * latticeT**2)/(latticeT+271) + 0.475*comp**2 # in eV, bandgap energy for InGaAs. 
        print(latticeT)

        # Creating new df to not mess with original 
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

        # Applying curve fit function 
        # DC-offset Correction 
        dc_guessb, dc_guessc, dc_fita, dc_fitb, dc_fitc, fig = guess_check('DC-Offset Calculations', new_df['Photon Energy'], new_df['S2c'], 'S2c', 'S2c fit', 'DC-Offset Fit', bandE)
        # Since dLambda to dE correction is already done with another column, we can skip straight to multiplier correction 

        # Multiplier Correction 
        new_df['Corrected S2'] = (new_df['dE_Conv S2'] - dc_fita) * new_df['Multiplier']
        guessb, guessc, final_a, final_b, final_c, fig = guess_check('Final Fit Calculation', new_df['Photon Energy'], new_df['Corrected S2'], 'Corrected S2', 'Corrected fit', 'Final Fit', bandE)
        e_temp = 1/(k*final_b)
        print(f"The carrier temperature is {e_temp} K.")
        print(new_df['Multiplier'])
        print(new_df['dE_Conv S2c'])
        print(new_df['dE_Conv S2'])


