import sys, os
import numpy as np

if len(sys.argv) != 3:
    print("Usage: add_fitness.py total_gens npop")
    exit(1)


for gen in range(int(sys.argv[1])):
    fitnesses = np.loadtxt("./Run_Outputs/rhino-sim/Generation_Data/"+str(gen)+"_fitnessScores.csv")
    for indiv in range(int(sys.argv[2])):
        png_file = "./Run_Outputs/rhino-sim/plot_files/"+str(gen)+"_plot_files/"+str(indiv)+"/"+str(gen)+"_"+str(indiv)+"_1.png"
        
        # Add fitness
        os.system("convert "+png_file+" -pointsize 14 -annotate +290+440 'Fitness = "+str(round(fitnesses[indiv], 2))+"' -trim "+png_file[:-4]+"_af.png")
        
