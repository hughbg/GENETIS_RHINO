import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import glob, copy
import fitness_calc
import plotting


names = [ "gauss", "peak", "symmetrical", "decreasing", "good_compare", "av" ] 

def setup_movie(unfits, index):
    '''Order the files by unfitness[index]. Most to least unfit. Create a command
    to make a movie. im_files just has a list of file names. Unfitnesses "unfits" 
    is a 2-D list with each index i being a list of unfitnesses. They have the average score 
    plus im_file index added to them so a row is like [gauss, peek, ... av, i]'''

    def check_nan(val):
        if np.isnan(val): return 1e39
        else: return val

    sorted_im_files = sorted(unfits, key=lambda el: check_nan(unfits[el][index]), reverse=True)  # greatest to least unfitness

    command = "convert -delay 20 "+" ".join(sorted_im_files)+" horn_batch_score_"+names[index]+".mp4"
    with open("horn_batch_command_"+names[index], "w") as f:
        for im_file in sorted_im_files:
            f.write("# "+im_file+" "+str(unfits[im_file][index])+"\n")
        f.write(command+"\n")

    os.system("zip horn_batch horn_batch_command_"+names[index])


def process_beams(path):
    '''
    Get the unfitnesses and make images.
    '''
    
    all_files = glob.glob(path)

    files = [ f for f in all_files if "_za.dat" not in f and  "_az.dat" not in f ]
    za_files = [ f for f in all_files if "_za.dat" in f ]
    az_files = [ f for f in all_files if "_az.dat" in f ]

    assert len(files) == len(az_files) and len(files) == len(za_files)
    print("Getting ", len(files), "beams")

    unfits_by_file = {}
    for i in range(len(files)):

        print(i, end=" "); sys.stdout.flush()

        # These are raw values that may include NaNs
        unfit = fitness_calc.unfitness(files[i], az_files[i], za_files[i])
        unfit.append(np.nanmean(unfit))
        
        image_file = os.path.basename(files[i])[:-4]+".png"
        unfits_by_file[image_file] = unfit+[np.nanmean(unfit)]   
        
        # For plot
        unfit_str = str([ np.round(f, 2) for f in unfit ])        
 
        if True:                    # switch plotting on/off
            plt.clf()
            plotting.plot_beam(files[i], az_files[i], za_files[i], name=os.path.basename(files[i])+"\n"+unfit_str, 
                               normalize=True, interpolation=None, save_to=image_file)

            os.system("convert "+image_file+" -trim x.png; mv x.png "+image_file)

    return unfits_by_file, len(unfit)
    

if not os.path.exists("movie_images"): os.mkdir("movie_images")
os.chdir("movie_images")

unfitnesses_by_image, num_scores = process_beams("/users/PAS1960/hughgarsden/GENETIS_PUEO_rhino/Run_Outputs/rhino-sim/dat_files/*_dat_files/*/*.dat")

print()

if os.path.exists("horn_batch.zip"): os.remove("horn_batch.zip")
os.system("zip horn_batch "+" ".join(unfitnesses_by_image))

# Do the fiducials. 
f_unfitnesses_by_image, _ = process_beams("/users/PAS1960/hughgarsden/GENETIS_PUEO_rhino/fiducial_beams/*.dat")


for i in range(num_scores):     
    print("Movie", i)
    _unfitnesses_by_image = unfitnesses_by_image.copy()
    if i == 0:  # gauss
       _unfitnesses_by_image["gauss.png"] = f_unfitnesses_by_image["gauss.png"]
    elif i == 1:  # peak
       _unfitnesses_by_image["peak_good.png"] = f_unfitnesses_by_image["peak_good.png"]
       _unfitnesses_by_image["peak_bad.png"] = f_unfitnesses_by_image["peak_bad.png"]

    elif i == 2:  # symmetrical
       _unfitnesses_by_image["symmetrical_good.png"] = f_unfitnesses_by_image["symmetrical_good.png"]
       _unfitnesses_by_image["symmetrical_bad.png"] = f_unfitnesses_by_image["symmetrical_bad.png"]
    elif i == 3:  # decreasing
       _unfitnesses_by_image["decreasing_good.png"] = f_unfitnesses_by_image["decreasing_good.png"]
       _unfitnesses_by_image["decreasing_bad.png"] = f_unfitnesses_by_image["decreasing_bad.png"]
    elif i == 4:  # good_compare
       _unfitnesses_by_image["matlab_horn_351MHz_rot.png"] = f_unfitnesses_by_image["matlab_horn_351MHz_rot.png"]


    setup_movie(_unfitnesses_by_image, i)   

# Extract the unfitness values and do some stats
unfitnesses_by_image = np.array([ unfit for key, unfit in unfitnesses_by_image.items() ])
np.savetxt("unfitnesses_by_image.txt", unfitnesses_by_image)
fits_by_file = fitness_calc.unfitness_to_fitness(unfitnesses_by_image)
np.savetxt("fits_by_file.txt", fits_by_file)

exit()
# Various plots

# Histograms of the unnormalized unfitness scores. 
for i in range(len(names)):
    plt.clf()
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)

    u = np.nan_to_num(unfitnesses_by_image[:, i], nan=np.nanmax(unfitnesses_by_image[:, i])*1.1)  # 1.1 to get Nans most unfit
    hist, bin_edges = np.histogram(u, bins="auto")
    bins = (bin_edges[1:]+bin_edges[:-1])/2
    plt.plot(bins, hist, lw=0.5)    
    plt.title("Hist unfitness score: "+names[i])
    plt.xlabel("Unfitness value")


    plt.subplot(1, 2, 2)
    hist, bin_edges = np.histogram(fits_by_file[:, i], bins="auto")
    bins = (bin_edges[1:]+bin_edges[:-1])/2
    plt.plot(bins, hist, lw=0.5)    
    plt.title("Hist fitness score: "+names[i])
    plt.xlabel("Fitness value")
    
    plt.savefig("histogram_score_"+names[i])
    os.system("zip horn_batch histogram_score_"+names[i]+".png")
    



plt.clf()
plt.figure(figsize=(16, 12))

# unfits and fits for each measure over the individuals
plt.subplot(2, 1, 1)
for i in range(len(unfitnesses_by_image[0])-1):
    plt.plot(unfitnesses_by_image[:, i], label=str(names[i]))
plt.legend()


plt.subplot(2, 1, 2)
for i in range(len(fits_by_file[0])-1):
    plt.plot(fits_by_file[:, i], label=str(names[i]))
plt.legend()
plt.savefig("scores_over_time")    # If some scores correlate with others then redundancy

os.system("zip horn_batch scores_over_time.png fits_by_file.txt unfitnesses_by_image.txt")

#os.system("rm "+" ".join(image_list))
