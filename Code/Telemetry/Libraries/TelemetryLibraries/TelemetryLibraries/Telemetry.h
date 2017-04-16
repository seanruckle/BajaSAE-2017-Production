#pragma once

#include "State.h"
#include "Display.h"
#include "Sensors.h"

class Telemetry
{
public:
	Telemetry();
	~Telemetry();


private:
	// Stores the state of the vehicle
	State state;

	// Show stuff to the user
	Display display;

	// Gathers data asynchronously
	// TODO: implement change notification
	Sensors sensors;
};

