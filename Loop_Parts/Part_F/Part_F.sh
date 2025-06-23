######### XF output conversion code (C)  ###########################################################################################
#
#
#         1. Converts .uan file from XF into a readable .dat file that Arasim can take in.
#s
#
####################################################################################################################################
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


chmod -R 777 $WorkingDir/Antenna_Performance_Metric
cd $WorkingDir/Antenna_Performance_Metric

mkdir -p $WorkingDir/Run_Outputs/$RunName/plot_files/${gen}_plot_files 2>/dev/null
for i in `seq 0 $((NPOP-1))`
do
  mkdir -p $WorkingDir/Run_Outputs/$RunName/plot_files/${gen}_plot_files/$i  2>/dev/null
done

dat_files=`find $WorkingDir/Run_Outputs/$RunName/dat_files/${gen}_dat_files -name '*.dat' ! -name '*_az.dat' ! -name '*_za.dat'`


for dat_file in $dat_files
do
   dat_name=`basename dat_file`
   python plotting.py $dat_file # > $RunDir/Errs_And_Outs/PlotOuts/${dat_name}.output 2>$RunDir/Errs_And_Outs/PlotOuts/${dat_name}.error
   check_exit_status "Plot $dat_file failed"
done

