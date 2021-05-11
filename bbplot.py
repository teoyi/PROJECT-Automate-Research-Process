import numpy as np 
import matplotlib.pyplot as plt 

h = 6.626*10**-34
c = 3.0*10**8
k = 1.38*10**-23

def planck(wav, T):
    a = (2*h*c**2)/wav**5
    b = h*c/(wav*k*T)
    intensity = a*(1/(np.exp(b)-1))
    return intensity

# generate x-axis in increments from 1nm to 3 micrometer in 1 nm increments
# starting at 1 nm to avoid wav = 0, which would result in division by zero.
wavelengths = np.arange(1*10**-9, 20*10**-6, 1*10**-9) 
temp1 = 202+273.15
temp2 = 23+273.15  

# intensity at 4000K, 5000K, 6000K, 7000K
intensity202 = planck(wavelengths, temp1)
intensity23 = planck(wavelengths, temp2)

plt.plot(wavelengths*1*10**9, intensity202, 'r-', label='202$^o C$') 
plt.plot(wavelengths*1*10**9, intensity23, 'b-', label='23$^o C$') 
plt.legend()
plt.ylabel('Emission Intensity (a.u.)')
plt.xlabel('Wavelength (nm)')
plt.show()
