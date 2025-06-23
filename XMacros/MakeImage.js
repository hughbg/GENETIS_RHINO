function MakeImage(i)
{

  function photo(cam, which) {
	  // Adjusts project camera to the above coordinates
	  View.setCamera(cam);
	  // Zooms out to include the entire detector, then saves as a .png
	  View.zoomToExtents();
	  View.setActiveScaleBarVisible(true);
	  View.setMeshVisible(true);
	  View.setPartsOpacity(50);
	  //View.setSensorsVisible(true);
	  View.saveImageToFile(workingdir+"/Run_Outputs/"+RunName+"/Antenna_Images/"+gen+"/"+i+"_"+"detector_"+which+".png", -1, -1);
  }


  // This function orients the generated detector and saves it as a .png
  // Creates a new Camera and initializes its position
  if (i==0)
  {
    newCam1 = Camera();
    newCam1.setPosition(Cartesian3D('2','2','10'))
    newCam2 = Camera();
    newCam2.setPosition(Cartesian3D('10','2','2'))
    newCam3 = Camera();
    newCam3.setPosition(Cartesian3D('2','10','2'))
    newCam4 = Camera();
    newCam4.setPosition(Cartesian3D('2','2','-10'))

  }

  photo(newCam1, "a");
  photo(newCam2, "b");
  photo(newCam3, "c");
  photo(newCam4, "d");


}
