// Make a waveguide
function build_waveguide(S,D) 
{
		// HG
        // s - sidelength
		// D - waveguide length     "depth", should be negative
        //var X0=[];    // distance from center of ridges at bottom // previously 0.04
        //var Y0=[];    // (half) width of ridges at bottom // previously 0.04
        // D is depth but is fixed it is also negative
        
	// Make the edges to define the square
	var edge1 = Line( new Cartesian3D(-S/2,-S/2, 0), new Cartesian3D(-S/2, S/2, 0));
	var edge2 = Line( new Cartesian3D(-S/2, S/2, 0), new Cartesian3D(S/2, S/2, 0));
	var edge3 = Line( new Cartesian3D(S/2, S/2, 0), new Cartesian3D(S/2, -S/2, 0));
	var edge4 = Line( new Cartesian3D(S/2, -S/2, 0), new Cartesian3D(-S/2, -S/2, 0));
	
	// Declare sketches to be made from the edges
	var wallSegment = new Sketch();
	var bottomSegment = new Sketch();
	wallSegment.addEdge(edge1);
	wallSegment.addEdge(edge2);
	wallSegment.addEdge(edge3);
	wallSegment.addEdge(edge4);

	var edge1 = Line( new Cartesian3D(-S/2,-S/2, D), new Cartesian3D(-S/2, S/2, D));
	var edge2 = Line( new Cartesian3D(-S/2, S/2, D), new Cartesian3D(S/2, S/2, D));
	var edge3 = Line( new Cartesian3D(S/2, S/2, D), new Cartesian3D(S/2, -S/2, D));
	var edge4 = Line( new Cartesian3D(S/2, -S/2, D), new Cartesian3D(-S/2, -S/2, D));

	bottomSegment.addEdge(edge1);
	bottomSegment.addEdge(edge2);
	bottomSegment.addEdge(edge3);
	bottomSegment.addEdge(edge4);


	// Let's start by making the bottom
	var bottomCover = new Cover(bottomSegment);
	var bottomRecipe = new Recipe();
	bottomRecipe.append( bottomCover );
	var bottomModel = new Model();
	bottomModel.setRecipe( bottomRecipe );
	// Add the surface
	var bottom = App.getActiveProject().getGeometryAssembly().append(bottomModel);
	bottom.name = "Bottom square";

	// Now we need to extrude the edges to get height
	var walls = new Extrude( wallSegment, D);				// Makes an Extrude
	var wallOptions = walls.getOptions();						// Gives the possible options for 
	// We will use the draft law option to extrude linearly
	wallOptions.draftOption = SweepOptions.DraftLaw;			// allows for draftlaw
	wallOptions.draftLaw = "(-1)";							// Set the expression for the extrude
	wallOptions.draftOption = 4;								// 4 indicates we use draftlaw
    //Walter - Change the gap type to Extended to get the desired shape
	wallOptions.gapType = SweepOptions.Extended; 				// I actually don't like this when we have x^2, but it doesn't do much for just x
    //Walter - Create a shell instead of a solid part
	wallOptions.createSolid = false;							// This way the shape isn't filled in
	walls.setOptions ( wallOptions );							// Sets the settings we assigned above

	// Make a recipe for a model
	var wallRecipe = new Recipe();
	wallRecipe.append(walls);
	var wallModel = new Model();
	wallModel.setRecipe(wallRecipe);
	wallModel.name = "Outer Walls";
	wallModel.getCoordinateSystem().translate(new Cartesian3D(0,0,0));	// Makes the model start at the origin

	// Set the material for these parts
	var wallProject = App.getActiveProject().getGeometryAssembly().append(wallModel);	// Adds the model to the project
	var pecMaterial = App.getActiveProject().getMaterialList().getMaterial( "PEC" );	// Makes the material available
	App.getActiveProject().setMaterial( wallProject, pecMaterial );						// Sets the material
	App.getActiveProject().setMaterial( bottom, pecMaterial );						// Sets the material

}
