######### XF output conversion code (C)  ###########################################################################################
#
#
#         1. Converts .uan file from XF into a readable .dat file that Arasim can take in.
#
#
####################################################################################################################################
#variables
WorkingDir=$1
RunName=$2
gen=$3

check_exit_status() {
    if [ $? -ne 0 ]; then
        echo $1
		exit 1
    fi
}

source $WorkingDir/Run_Outputs/$RunName/setup.sh




chmod -R 777 $WorkingDir/Antenna_Performance_Metric
cd $WorkingDir/Antenna_Performance_Metric


mkdir -p $WorkingDir/Run_Outputs/$RunName/dat_files/${gen}_dat_files 2>/dev/null
for i in `seq 0 $((NPOP-1))`
do
  mkdir -p $WorkingDir/Run_Outputs/$RunName/dat_files/${gen}_dat_files/$i  2>/dev/null
done

uan_files=`find $WorkingDir/Run_Outputs/$RunName/uan_files/${gen}_uan_files -name '*.uan'`

for uan_file in $uan_files
do 
   uan_name=`basename uan_file`
   python process_uan.py $uan_file #> $RunDir/Errs_And_Outs/DatOuts/${uan_name}.output 2>$RunDir/Errs_And_Outs/DatOuts/${uan_name}.error
   check_exit_status "UAN -> DAT converion failed" 
done


