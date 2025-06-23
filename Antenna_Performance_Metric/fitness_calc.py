import numpy as np
import sys, os
from scipy.optimize import curve_fit
from plotting import plot_beam
import numpy as np


def Gaussian_2d(x_y, A, mu_x, mu_y, sigma_x, sigma_y):
    G= A*np.exp(-(x_y[0]-mu_x)**2/(2*sigma_x**2) - (x_y[1]-mu_y)**2/(2*sigma_y**2) )
    return G



def load_power_norm(fname):
    data = np.loadtxt(fname, delimiter=",")
    assert np.min(data) >= 0, "Found -ve values in dat file - this is in dB"
    data /= np.max(data)
    return data

def flip_by_az(raw_beam):
    new_beam = np.zeros_like(raw_beam)
    
    for az in range(raw_beam.shape[1]):
        new_az = 180-az
        if new_az < 0: new_az = raw_beam.shape[1]+new_az
        #print(az, new_az)
        new_beam[:, new_az] = raw_beam[:, az]
        
    return new_beam
    
def diff_beams(b1, b2):
    '''If they are in db, a subtraction is a ratio of power'''
    diff = b1-b2
    #print("Max", np.max(diff), "min", np.min(diff))
    return np.sqrt(np.mean(diff**2))

def unfitness(data_file, az_file, za_file):

    ungridded = load_power_norm(data_file)
    az = np.loadtxt(az_file, delimiter=",")
    za = np.loadtxt(za_file, delimiter=",")
    az, za = np.meshgrid(za, az)
    za = np.ravel(za)
    az = np.ravel(az)
    
   # Cut some things where 360 goes to 0 and za 0-90
    ungridded = ungridded.ravel()
    ungridded = ungridded[(az<360) & (za<=90)]
    _za = za[(az<360) & (za<=90)]
    az = az[(az<360) & (za<=90)]
    za = _za

    # Calc x/y points
    za = np.deg2rad(za)
    az = np.deg2rad(az)
    r = np.sin(za)
    x = r*np.sin(az)
    y = r*np.cos(az)  


    # 1. Gauss fit
    try:
        p0 = np.array([1, 0, 0, 0.1, 0.1])
        popt, pcov = curve_fit(Gaussian_2d, (x, y), ungridded, p0)
        #print("popt", popt)
        #print("pcov diag", np.diag(pcov))
        #print("Error", np.max(np.sqrt(np.diag(pcov))))
    
        # Unfitness values means the higher the value, the more unfit. These are going to normalized
        # and reversed once all individuals are done.
        
        # Reconstruct the beam and compare to original
        gauss = Gaussian_2d((x, y), *popt)

        gauss_unfitness = np.sqrt(np.mean((ungridded-gauss)**2))
        
        #gauss_unfitness = np.max(np.sqrt(np.diag(pcov)))
    except:
        gauss_unfitness = np.nan     

    ungridded = load_power_norm(data_file)
    
    # 2. See if peak is in the middle
    peak_unfitness = 1-np.mean(ungridded[0])   # at za = 0 take average, should be 1 for peak at za=0
    
    # 3. See if symmetrical. This test is done on ungridded data which is converted to power
    # and normalized.
    diff_unfitness = diff_beams(ungridded, flip_by_az(ungridded))
    
    # 4. See if only decreasing power as za goes 0 -> 90. Done on ungridded data.
    decreasing_unfitness = 0
    for i in range(ungridded.shape[1]):
        diffs = np.diff(ungridded[:, i])
        decreasing_unfitness += len(diffs[diffs>0])/len(diffs)
    decreasing_unfitness /= ungridded.shape[0]
    
    # 5. Compare to a good beam that it's possible to generate
    good_ungridded = load_power_norm("/users/PAS1960/hughgarsden/matlab_beams/matlab_horn_351MHz_rot.dat")
    good_unfitness = diff_beams(ungridded, good_ungridded)

    return [ gauss_unfitness, peak_unfitness, diff_unfitness, decreasing_unfitness, good_unfitness ]



def unfitness_to_fitness(unfits):
    # unfits is array NxM where N is number of beams and M is number of scores per beam
    fits = np.zeros_like(unfits)
    
    # Convert to fitnesses for a measure. For each column (unfitness score), reverse the values so that they become a fitness
    # normalized to 1. Be careful of NaN.
    # Eg.   10, 9, 8, 7   goes to  0, 1, 2, 3   and then   0, 0.33, 0.66, 1
    for i in range(unfits.shape[1]):
        x = unfits[:, i]
        x = np.nan_to_num(np.nanmax(x)-x+0.01)  # 0.01 is so fitness doesn't go to 0, only if NaN
        x /= np.max(x)

        fits[:, i] = x
        
    return fits
        

def generation_fitness(working_dir, run_name, generation, population):

    path = working_dir+"/Run_Outputs/"+run_name+"/dat_files/"+generation+"_dat_files"

    unfitnesses = []

    for i in range(0, population):
        dat_path = path+"/"+str(i)+"/"+generation+"_"+str(i)+"_1"
        data = dat_path+".dat"   
        az = dat_path+"_az.dat"  
        za = dat_path+"_za.dat"  


        try:
            unfitnesses.append(unfitness(data, az, za))
        except:
            unfitnesses.append([np.nan, np.nan, np.nan, np.nan, np.nan])

    unfitnesses = np.array(unfitnesses)

    fitnesses = unfitness_to_fitness(unfitnesses)

    # Now everything normalized from 0 to 1 so take the mean over the different score types.
    # Or just pick out one.
    fitnesses = fitnesses[:, 0]  #np.mean(fitnesses, axis=1)

    # Write data to csv file
    print("Wrote", working_dir+"/Run_Outputs/"+run_name + "/Generation_Data" + f"/{generation}_fitnessScores.csv")
    np.savetxt(working_dir+"/Run_Outputs/"+run_name + "/Generation_Data" + f"/{generation}_fitnessScores.csv", fitnesses, delimiter=",")
    #np.savetxt("fitnessScores.csv", fitnesses, delimiter=",")
        
      
if __name__ == "__main__":
    # Args example /users/PAS1960/hughgarsden/GENETIS_PUEO_rhino rhino-sim 0 4      
    generation_fitness(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))

    #print(unfitness("./Run_Outputs/rhino-sim/dat_files/0_dat_files/2/0_2_1.dat", "./Run_Outputs/rhino-sim/dat_files/0_dat_files/2/0_2_1_az.dat", "./Run_Outputs/rhino-sim/dat_files/0_dat_files/2/0_2_1_za.dat"))

