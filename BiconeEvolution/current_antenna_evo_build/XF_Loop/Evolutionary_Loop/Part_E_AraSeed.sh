
########  Fitness Score Generation (E)  ######################################################################################################### 
#
#
#      1. Takes AraSim data and cocatenates each file name into one string that is then used to generate fitness scores 
#
#      2. Then gensData.py extracts useful information from generationDNA.csv and fitnessScores.csv, and writes to maxFitnessScores.csv and runData.csv
#
#      3. Copies each .uan file from the Antenna_Performance_Metric folder and moves to Run_Outputs/$RunName folder
#
#
#################################################################################################################################################### 

#variables
gen=$1
NPOP=$2
WorkingDir=$3
RunName=$4
ScaleFactor=$5
AntennaRadii=$6
indiv=$7
Seeds=$8
GeoFactor=$9
AraSimExec=${10}
XFProj=${11}

#chmod -R 777 /fs/project/PAS0654/BiconeEvolutionOSC/BiconeEvolution/

module load python/3.7-2019.10

cd Antenna_Performance_Metric/

echo 'Starting fitness function calculating portion...'

mv *.root "$WorkingDir/Run_Outputs/$RunName/RootFilesGen${gen}/"

for i in `seq $indiv $NPOP`
do
  	InputFiles="${InputFiles}AraOut_${gen}_${i}.txt " #had .txt but that's also in the fitnessfunction executable
       
done

./fitnessFunction.exe $NPOP $Seeds $ScaleFactor $AntennaRadii/generationDNA.csv $GeoFactor $InputFiles #Here's where we add the flags for the generation
cp fitnessScores.csv "$WorkingDir"/Run_Outputs/$RunName/${gen}_fitnessScores.csv
mv fitnessScores.csv "$WorkingDir"

cp vEffectives.csv "$WorkingDir"/Run_Outputs/$RunName/${gen}_vEffectives.csv
mv vEffectives.csv "$WorkingDir"

cp errorBars.csv "$WorkingDir"/Run_Outputs/$RunName/${gen}_errorBars.csv
mv errorBars.csv "$WorkingDir"

#Plotting software for Veff(for each individual) vs Generation
python Veff_Plotting.py "$WorkingDir"/Run_Outputs/$RunName "$WorkingDir"/Run_Outputs/$RunName $gen $NPOP $Seeds

cd "$WorkingDir"
if [ $gen -eq 0 ]
then
	rm runData.csv
fi

if [ $indiv -eq $NPOP ]
then
	mv runData.csv $WorkingDir/Run_Outputs/$RunName/runData_$gen.csv
fi

python gensData.py $gen 
cd Antenna_Performance_Metric
next_gen=$(($gen+1))
python LRTPlot.py "$WorkingDir" "$WorkingDir"/Run_Outputs/$RunName $next_gen $NPOP $GeoFactor

# Run 3D Plots of L,R,T vs Fitness
python 3DLength.py "$WorkingDir" "$WorkingDir"/Run_Outputs/$RunName $next_gen $NPOP $GeoFactor $NSECTIONS
python 3DRadius.py "$WorkingDir" "$WorkingDir"/Run_Outputs/$RunName $next_gen $NPOP $GeoFactor $NSECTIONS
python 3DTheta.py "$WorkingDir" "$WorkingDir"/Run_Outputs/$RunName $next_gen $NPOP $GeoFactor $NSECTIONS

cd ..


#we want to record the gain data each time
cd $AraSimExec
for i in `seq 1 $NPOP`
do
	mv a_${i}.txt $XFProj/XF_model_${gen}_$i.txt
done

cd $WorkingDir/Antenna_Performance_Metric

python3 avg_freq.py $XFProj $XFProj 10 $NPOP

cd $XFProj
mv gain_vs_freq.png gain_vs_freq_gen_$gen.png

echo 'Congrats on getting a fitness score!'

cd $WorkingDir/Run_Outputs/$RunName

mkdir -m777 AraOut_$gen
cd Antenna_Performance_Metric
for i in `seq 1 $NPOP`
do
    for j in `seq 1 $Seeds`
    do

	cp AraOut_${gen}_${i}_${j}.txt $WorkingDir/Run_Outputs/$RunName/AraOut_${gen}/AraOut_${gen}_${i}_${j}.txt
	
	done

done 

cd $WorkingDir

mv parents.csv Run_Outputs/$RunName/${gen}_parents.csv
mv genes.csv Run_Outputs/$RunName/${gen}_genes.csv
mv mutations.csv Run_Outputs/$RunName/${gen}_mutations.csv
mv generators.csv Run_Outputs/$RunName/${gen}_generators.csv

#chmod -R 777 /fs/project/PAS0654/BiconeEvolutionOSC/BiconeEvolution/
