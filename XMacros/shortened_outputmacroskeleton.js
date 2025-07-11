var simNum = "00"
if( k < 10){
var simNum = simNum + "000" + k;
}
else if ( k >= 10 && k < 100){
var simNum = simNum + "00" + k;
}
else if ( k >= 100 && k < 1000){
var simNum = simNum + "0" + k;
}
else{
var simNum = simNum + k;
}

var indiv_in_pop = ((k - 1) % popsize);

var query = new ResultQuery();
///////////////////////Get Theta and Phi Gain///////////////
query.projectId = App.getActiveProject().getProjectDirectory();

Output.println( App.getActiveProject().getProjectDirectory() );

query.runId = "Run0001";
query.simulationId = simNum;
query.sensorType = ResultQuery.FarZoneSensor;
query.sensorId = "Far Zone Sensor";
query.timeDependence = ResultQuery.SteadyState;
query.resultType = ResultQuery.RealizedGain;
query.fieldScatter = ResultQuery.TotalField;
query.resultComponent = ResultQuery.Theta;
query.dataTransform = ResultQuery.NoTransform;
query.complexPart = ResultQuery.NotComplex;
query.surfaceInterpolationResolution = ResultQuery.NoInterpolation;
query.setDimensionRange( "Frequency", 0, -1 );
query.setDimensionRange( "Theta", 0, -1 );
query.setDimensionRange( "Phi", 0, -1 );

var thdata = new ResultDataSet( "" );
thdata.setQuery( query );
if( !thdata.isValid() ){
Output.println( "1getCurrentDataSet() : " +
thdata.getReasonWhyInvalid() );
}

query.resultComponent = ResultQuery.Phi;
var phdata = new ResultDataSet("");
phdata.setQuery(query);

if( !phdata.isValid() ){
Output.println( "2getCurrentDataSet() : " +
phdata.getReasonWhyInvalid() );
}
/////////////////Get Theta and Phi Phase///////////////////////////////////

query.resultType = ResultQuery.E;
query.fieldScatter = ResultQuery.TotalField;
query.resultComponent = ResultQuery.Theta;
query.dataTransform = ResultQuery.NoTransform;
query.complexPart = ResultQuery.Phase;
query.surfaceInterpolationResolution = ResultQuery.NoInterpolation;
query.setDimensionRange( "Frequency", 0, -1 );
query.setDimensionRange( "Theta", 0, -1 );
query.setDimensionRange( "Phi", 0, -1 );


var thphase = new ResultDataSet("");
thphase.setQuery(query);

if( !thphase.isValid() ){
Output.println( "3getCurrentDataSet() : " +
thphase.getReasonWhyInvalid() );
}

query.resultComponent = ResultQuery.Phi;
query.ComplexPart = ResultQuery.Phase;
var phphase = new ResultDataSet("");
phphase.setQuery(query);

if( !phphase.isValid() ){
Output.println( "4getCurrentDataSet() : " +
phphase.getReasonWhyInvalid() );
}

/////////////////Get Input Power///////////////////////////
query.sensorType = ResultQuery.System;
query.sensorId = "System";
query.timeDependence = ResultQuery.SteadyState;
query.resultType = ResultQuery.NetInputPower;
query.fieldScatter = ResultQuery.NoFieldScatter;
query.resultComponent = ResultQuery.Scalar;
query.dataTransform = ResultQuery.NoTransform;
query.complexPart = ResultQuery.NotComplex;
query.surfaceInterpolationResolution = ResultQuery.NoInterpolation;
query.clearDimensions();
query.setDimensionRange("Frequency",0,-1);

var inputpower = new ResultDataSet("");
inputpower.setQuery(query);
if( !inputpower.isValid() ){
Output.println( "5getCurrentDataSet() : " +
inputpower.getReasonWhyInvalid() );
}
for (var i = 0; i < freqs; i++){
var file = rundir + "/uan_files/" + gen + "_uan_files/" + indiv_in_pop;
file = file + "/" + gen + "_" + indiv_in_pop + "_" + (i+1) + ".uan"
Output.println(file);
FarZoneUtils.exportToUANFile(thdata,thphase,phdata,phphase,inputpower,file, i);
}
}
App.quit();
