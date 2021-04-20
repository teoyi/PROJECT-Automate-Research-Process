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

rt_band = input("Eg at room temp:")

'''
**** SECTION 1 ****
This section contains mathematical functions to calculate values to be used.
1. Composition Solver 
2. Curve fit function 
'''
# Using python to solve for quadratic equation 
# Note that Eg is found through the excel sheet 
# Eg is found at ambient temperature of 298K 
# quad_E  = 0.475*x**2 + (0.625*(5.8/(latticeT+300)-4.19/(latticeT+271))*10**-4 * latticeT**2)*x + (0.42 - (4.19*10**-4 * latticeT**2)/(latticeT+271) - rt_band) 
# This quadratic equation is taken from http://www.ioffe.ru/SVA/NSM/Semicond/GaInAs/bandstr.html


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
        print(f"The composition is: {ans10.real}.")
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
    plt.savefig(path2 + f"/{dirName2}/{plot_title}")
    plt.close(fig)
    return p0_b, p0_c, pfinal_a, pfinal_b, pfinal_c, fig


