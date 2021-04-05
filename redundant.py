# Converting raw S2c to semi log plot of emission intensity against photon energy  (log scale with matplotlib)
plt.plot(new_df['Photon Energy'], new_df[col[1]], 'o', label='S2c')
plt.plot(new_df['Photon Energy'], new_df[col[3]], 'o', label='S2')
plt.ylabel('Emission Intensity (a.u.)')
plt.xlabel('Photon Energy (eV)')
plt.yscale('log')
plt.legend()
plt.savefig('semilog.png')
plt.show()

# Applying curve fit to S2c data to determine DC offset = a
def fit(E,a,b): 
    return E*np.sqrt(E-bandE)*np.exp(-E/(k*b)) # Eg and k are already defined previously 

E = np.linspace(np.min(new_df['Photon Energy']), np.max(new_df['Photon Energy']),1000)
popt, pcov = curve_fit(fit, new_df['Photon Energy'], new_df[col[1]], maxfev = 5000) # note: col[1] is S2c column 

print(popt)
print(pcov)

#__________________________________________________________#

# Applying curve fit to S2c data to determine DC offset = a
# Solving for a to begin second correction, the DC offset 
def ln_fit(E,a,b): 
    return a+0.5*np.log(E-bandE)-(E/(k*b)) # Eg and k are already defined previously 

E = np.linspace(np.min(new_df['Photon Energy']), np.max(new_df['Photon Energy']),1000)

popt, pcov = curve_fit(ln_fit, new_df['Photon Energy'], new_df['ln(S2c)'], maxfev = 5000) # note: col[1] is S2c column 

print(f"The DC offset of this data is {popt[0]}")
dc_offset = popt[0]
plt.plot(new_df['Photon Energy'], new_df['ln(S2c)'], 'o', label='S2c')
plt.plot(new_df['Photon Energy'], ln_fit(new_df['Photon Energy'], *popt), '-', label='S2c fit')
plt.ylabel('Emission Intensity (a.u.)')
plt.xlabel('Photon Energy (eV)')
plt.legend()
#plt.savefig('fit.png')
plt.show()

print(dc_offset)

# Applying 3rd correction, multiplier, to determine the corrected S2 values 
new_df['Multiplier'] = new_df['S2c']/new_df['S2']
#print(new_df)
new_df['Corrected S2'] = (new_df['S2'] - dc_offset)*new_df['Multiplier']
new_df['ln(Corrected S2)'] = np.log10(new_df['Corrected S2'])
print(new_df)

plt.plot(new_df['Photon Energy'], new_df['Corrected S2'],'o', label='Corrected S2')
plt.plot(new_df['Photon Energy'], new_df['ln(Corrected S2)'],'o', label='Corrected S2')
plt.yscale('log')
plt.ylabel('Emission Intensity (a.u.)')
plt.xlabel('Photon Energy (eV)')
plt.legend()
plt.savefig('correctedsmilog.png')
plt.show()