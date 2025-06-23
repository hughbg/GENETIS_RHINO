
########  Fitness Score Generation (E)  ######################################################################################################### 
#
#
#      1. Takes the root files from the generation and runs rootAnalysis.py on them to get the fitness scores
#
#      2. Then gensData.py extracts useful information from generationDNA.csv and fitnessScores.csv, and writes to maxFitnessScores.csv and runData.csv
#
#
#################################################################################################################################################### 

#variables
WorkingDir=$1
RunName=$2
gen=$3
source $WorkingDir/Run_Outputs/$RunName/setup.sh

check_exit_status() {
    if [ $? -ne 0 ]; then
        echo $1
		exit 1
    fi
}


echo 'Starting fitness function calculating portion...'

cd $WorkingDir/Antenna_Performance_Metric
python fitness_calc.py $WorkingDir $RunName $gen $NPOP
check_exit_status "Fitness calc failed"
