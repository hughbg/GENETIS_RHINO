"""
To do:
Pay attention to the values in the header, at moment assumptions are made
"""

import numpy as np
import yaml, sys

def strip_header(fname):
    phi_inc = theta_inc = magnitude = None    # need these to process the file
    f = open(fname)
    line = f.readline()
    while "end_<parameters>" not in line:
        if "phi_inc" in line:
            phi_inc = int(line.split()[1])
        if "theta_inc" in line:
            theta_inc = int(line.split()[1])
        if "magnitude" in line:
            magnitude = line.split()[1]

        line = f.readline()

    assert phi_inc is not None and theta_inc is not None and magnitude is not None, "required headers missing"

    return f, phi_inc, theta_inc, magnitude


dB_to_lin = lambda vals: 10**(vals/10)
no_change = lambda vals: vals

to_power = lambda efield : (efield[0]*np.conj(efield[0])+efield[1]*np.conj(efield[1])).real
 
# amp in dB and phase in degree
polar_to_re_im = lambda f, amp, phase: f(amp)*(np.cos(np.deg2rad(phase))+np.sin(np.deg2rad(phase))*1j)

values_file, za_inc, az_inc, magnitude = strip_header(sys.argv[1])
uan_values = np.loadtxt(values_file)



za = np.sort(np.unique(uan_values[:, 0])).astype(int)
az = np.sort(np.unique(uan_values[:, 1])).astype(int)


scale = no_change
if magnitude == "dB":
    scale = dB_to_lin

# (Naxes_vec, 1, Nfeeds or Npols, Nfreqs, Naxes2, Naxes1)
values = np.zeros((za.size, az.size))      
for i in range(uan_values.shape[0]):
    _za = int(uan_values[i, 0])
    _az = int(uan_values[i, 1])
    E_za = polar_to_re_im(scale, uan_values[i, 2], uan_values[i, 4])
    E_az = polar_to_re_im(scale, uan_values[i, 3], uan_values[i, 5])
    assert values[_za//za_inc, _az//az_inc] == 0, str(_az)+" Already has a value"

    values[_za//za_inc, _az//az_inc] = to_power((E_az, E_za))

assert np.min(values) != 0

# Data
with open(sys.argv[1][:-4].replace("uan", "dat")+".dat", "w") as f:
	for i in range(za.size):
		for j in range(az.size-1):
		    f.write(str(values[i, j])+",")
		f.write(str(values[i, -1])+"\n")

with open(sys.argv[1][:-4].replace("uan", "dat")+"_az.dat", "w") as f:
    for i in range(az.size-1):
        f.write(str(az[i])+",")
    f.write(str(az[-1])+"\n")

with open(sys.argv[1][:-4].replace("uan", "dat")+"_za.dat", "w") as f:
    for i in range(za.size-1):
        f.write(str(za[i])+",")
    f.write(str(za[-1])+"\n")



