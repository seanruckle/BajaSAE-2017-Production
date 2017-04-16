#pragma once

/*	This file contains all of the configuration options available for the telemetry system
	A separate program may be written to recompile the telemetry code with different configurations	*/

// Display modes
#define _DISPLAY_MODE_HEADLESS		(1<<0)
#define _DISPLAY_MODE_CONSOLE		(1<<1)
#define _DISPLAY_MODE_DRIVER		(1<<2)
#define _DISPLAY_MODE_DIAGNOSTIC	(1<<3)
#define _DISPLAY_MODE_OVERLAY		(1<<4)
#define _DISPLAY_MODE_SERVER		(1<<5)
#define _DISPLAY_MODE_CLIENT		(1<<6)
#define _DISPLAY_MODE_VARIABLE		(1<<7)

// Available Sensors
#define _SENSOR_ENABLED_GPS			
#define _SENSOR_ENABLED_IMU
#define _SENSOR_ENABLED_TEMP
#define _SENSOR_ENABLED_RPM
#define _SENSOR_ENABLED_BRAKES
#define _SENSOR_ENABLED_FROM_FILE
#define _SENSOR_ENABLED_FROM_REMOTE


// 




