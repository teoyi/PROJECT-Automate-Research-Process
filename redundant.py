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