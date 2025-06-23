/**************************************** Set Global Variables **************************************************/
var units = " m";
var path = workingdir + "/Run_Outputs/" + RunName + "/Generation_Data/" + gen + "_generationDNA.csv"


// Order of genes:
// flare_length, flare_side, waveguide_length, waveguide_side

// create the frequency array, these are in MHz which is set at FOI.addSpecifiedFrequency(freq[k] + " MHz");
var freq = [];
for (var i = 0; i < freqCoefficients; i++) {
    freq.push(freq_start + i * freq_step);
}

/******************************************** Read in Data *****************************************************/
var antennaLines = 0 // This is how many lines come before the antenna data
var file = new File(path);
file.open(1);
var generationDNA = file.readAll();
