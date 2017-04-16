#pragma once

#define BUFFER_SIZE 255
class GenericSensor
{
public:
	GenericSensor();
	~GenericSensor();
	// returns a string with data in it
	void getDataAsString(char (&buffer)[BUFFER_SIZE], unsigned int len);
	// returns a value corresponding to the named parameter
	int getValue(unsigned char name);
};

