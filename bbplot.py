import numpy as np 
import matplotlib.pyplot as plt 
from sklearn import preprocessing

h = 6.626*10**-34
c = 3.0*10**8
k = 1.38*10**-23

def planck(wav, T):
    a = (2*h*c**2)/wav**5
    b = h*c/(wav*k*T)
    intensity = a*(1/(np.exp(b)-1))
    return intensity

k1 = 8.617333262145 * 10 ** -5 # Boltzmann constant in eV/K

def fit(wav, T, Eg):
    lamb = wav*1*10**9 #convert m to nm 
    g = -1240/(lamb*k1*T)
    intensity = ((1240/lamb)*np.sqrt((1240/lamb)-Eg)*np.exp(g))
    return intensity

# generate x-axis in increments from 1nm to 3 micrometer in 1 nm increments
# starting at 1 nm to avoid wav = 0, which would result in division by zero.
# wavelengths = np.arange(1*10**-9, 3*10**-6, 1*10**-9) 
wavelengths = np.arange(1*10**-6, 3*10**-6, 1*10**-9) 
temp1 = 202+273.15
temp2 = 23+273.15  

intensity202 = planck(wavelengths, temp1)
intensity23 = planck(wavelengths, temp2)
intensity1550 = fit(wavelengths, temp2, 0.785)
intensity1650 = fit(wavelengths, temp2, 0.74)

i1550_masked = np.ma.array(intensity1550, mask=np.isnan(intensity1550))
print(i1550_masked)

norm_i202 = intensity202/np.linalg.norm(intensity202)
norm_i23 = intensity23/np.linalg.norm(intensity23)
norm_i1550 = intensity1550/np.sqrt(np.nansum(np.square(intensity1550)))
norm_i1650 = intensity1650/np.sqrt(np.nansum(np.square(intensity1650)))

print(norm_i1650)
plt.plot(wavelengths*1*10**9, intensity202)
plt.plot(wavelengths*1*10**9, intensity23)
plt.plot(wavelengths*1*10**9, norm_i1550*1*10**4)
plt.plot(wavelengths*1*10**9, norm_i1650*1*10**4)
plt.yscale('log')
plt.show()
# plt.plot(wavelengths*1*10**9, intensity202, 'r-', label='202$^o C$') 
# plt.plot(wavelengths*1*10**9, intensity23, 'b-', label='23$^o C$') 
# plt.plot(wavelengths*1*10**9, intensity1650/intensity1650[-1], color='red', label='1650$nm$ at 202$^oC$')
# plt.plot(wavelengths*1*10**9, intensity1550/intensity1550[-1], color='green', label='1550$nm$ at 202$^oC$')
# plt.legend()
# plt.ylabel('Emission Intensity (a.u., normalized)')
# plt.xlabel('Wavelength (nm)')
# plt.show()

# print(intensity1650)
# plt.plot(wavelengths*1*10**9, intensity1650)
# plt.plot(wavelengths*1*10**9, intensity1550)
# plt.show()


