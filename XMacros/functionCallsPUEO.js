/********************************************* Function Calls **************************************************/
var file = new File(path);
file.open(1);
var generationDNA = file.readAll();

// Lists to hold the genes flare_length, flare_side, waveguide_length, waveguide_side
var flare_length=[];	// Matlab terminology, flare is the horn
var flare_side=[];	// flare is square
var waveguide_length=[];	
var waveguide_side=[];	

var lines = generationDNA.split('\n');

// Loop over reading in the gene values
for(var i = 0;i < lines.length - 1;i++){
	if(i>=antennaLines){
		var params = lines[i].split(",");
		/*Output.println("Individual "+ i);
		Output.println("flare length: "+params[0]);
		Output.println("flare side: "+params[1]);
		Output.println("waveguide length: "+params[2]);
		Output.println("waveguide side: "+params[3]);
		*/
		flare_length[i-antennaLines]=params[0]
		flare_side[i-antennaLines]=params[1]
		waveguide_length[i-antennaLines]=params[2]
		waveguide_side[i-antennaLines]=params[3]

	}
}

for(var i = indiv - 1; i < NPOP; i++)
{
	
		var fl = flare_length[i];
		var fs = flare_side[i]
		var wl = waveguide_length[i]
		var ws = waveguide_side[i]


		Output.println("flare_length: "+ fl);
		Output.println("flare_side: "+ fs);
		Output.println("waveguide_length: "+ wl);
		Output.println("waveguide_side: "+ ws);

		// Function calls
		// We do it twice, first for horizontal source then for vertical
		// HG just once
		for(var k = 0; k < 1; k++)
		{

			App.getActiveProject().getGeometryAssembly().clear();
			CreatePEC();
			build_waveguide(1.0*ws, -1.0*wl);
			build_walls(ws, fs, fl);
			CreateAntennaSource(k, 1.0*ws, -1.0*wl); 
			CreateGrid();
			CreateSensors();
			CreateAntennaSimulationData();
			QueueSimulation();
			Output.println(ResultQuery().simulationId);
			MakeImage(i);
		}
		
	
}

file.close();
App.quit();
