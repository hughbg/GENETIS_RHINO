// Make the grid
function CreateGrid()
{

    // Set up the grid spacing for the antenna

    var grid = App.getActiveProject().getGrid();
    var cellSizes = grid.getCellSizesSpecification();
/*
    cellSizes.setTargetSizes( Cartesian3D( "6 cm", "6 cm", "6 cm" ));
    // And we need to set the Minimum Sizes - these are the minimum deltas that we will allow in this project.
    // We'll use the scalar ratio of 20% here.   
    cellSizes.setMinimumSizes( Cartesian3D( ".5", ".5", ".5" ) );
    cellSizes.setMinimumIsRatioX( true );
    cellSizes.setMinimumIsRatioY( true );
    cellSizes.setMinimumIsRatioZ( true );

    grid.specifyPaddingExtent( Cartesian3D( "1", "1", "1" ), Cartesian3D( "1", "1", "1" ), true, true );
*/
	Output.println("num x cells: "+grid.getXCellCount());
	Output.println("num y cells: "+grid.getYCellCount());
	Output.println("num z cells: "+grid.getZCellCount());
	Output.println("pro grid enabled: "+grid.proGridEnabled);
	Output.println("target sizes: "+cellSizes.getTargetSizes());


}

