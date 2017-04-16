#include "GenericSensor.h"



GenericSensor::GenericSensor()
{
}


GenericSensor::~GenericSensor()
{
}


// returns a string with data in it
void GenericSensor::getDataAsString(char (&buffer)[BUFFER_SIZE], unsigned int len)
{
	return;
}


// returns a value corresponding to the named parameter
int GenericSensor::getValue(unsigned char name)
{
	return 0;
}
