
// Make the sensors to detect the emitted signal
function CreateSensors()
{
    // Here we will create a sensor definition and attach it to a near-field sensor on the surface of one of our objects.

    var sensorDataDefinitionList = App.getActiveProject().getSensorDataDefinitionList();
        sensorDataDefinitionList.clear();

    // Create a sensor
	var angleIncrementDegrees = 1;
	var angleIncrementRadians = angleIncrementDegrees*Math.PI/180

    var farSensor = new FarZoneSensor();
    farSensor.retrieveSteadyStateData = true;
    farSensor.setAngle1IncrementRadians(angleIncrementRadians);
    farSensor.setAngle2IncrementRadians(angleIncrementRadians);
    farSensor.name = "Far Zone Sensor";


    var FarZoneSensorList = App.getActiveProject().getFarZoneSensorList();
    FarZoneSensorList.clear();
    FarZoneSensorList.addFarZoneSensor( farSensor );
}
