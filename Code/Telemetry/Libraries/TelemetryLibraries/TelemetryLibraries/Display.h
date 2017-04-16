#pragma once
#include "State.h"
class Display
{
public:
	Display();
	Display(unsigned char mode);
	~Display();
	// Set the display mode
	void setMode(unsigned char mode);
	// Return current display mode
	unsigned char getMode();
	// Set speed to display (Not the speed of the screen)
	void setSpeed(unsigned char speed);
	// set turn signal direction
	void setSignal(unsigned char direction);
	// Set data source
	void setSource(State & state);

	void showState(State & state);
	
private:
	unsigned char speed;
	unsigned char signal;
	unsigned char mode;
	
	// TODO: figure out how to store references
	//State state;
	// perform any necessary setup
	void init();
};

