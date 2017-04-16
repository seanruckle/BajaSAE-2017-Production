#include "dictionary.h"
#include "Display.h"
#include "API_Generic\SerialGraphicLCD.h"


LCD lcd;

Display::Display()
{
// TODO: add LCD init function
}

Display::Display(unsigned char mode)
{
	setMode(mode);
	switch (mode) {
	case _DISPLAY_MODE_HEADLESS:
		break;
	case _DISPLAY_MODE_CONSOLE:
		break;
	case _DISPLAY_MODE_DRIVER:
		
		break;
	case _DISPLAY_MODE_DIAGNOSTIC:
		break;
	case _DISPLAY_MODE_OVERLAY:
		break;
	case _DISPLAY_MODE_SERVER:
		break;
	case _DISPLAY_MODE_CLIENT:
		break;
	case _DISPLAY_MODE_VARIABLE:
		break;
	default:
		break;

	}

}


Display::~Display()
{
}


// Set the display mode
void Display::setMode(unsigned char mode)
{

}


// Return current display mode
unsigned char Display::getMode()
{
	return mode;
}


// Set speed to display (Not the speed of the screen)
void Display::setSpeed(unsigned char speed)
{
}


// set turn signal direction
void Display::setSignal(unsigned char direction)
{
}

void Display::setSource(State & state)
{

}

void Display::showState(State & state)
{
	switch (mode) {
	case _DISPLAY_MODE_HEADLESS:
		break;
	case _DISPLAY_MODE_CONSOLE:
		break;
	case _DISPLAY_MODE_DRIVER:
		lcd.drawBig(state.getSpeed());
		break;
	case _DISPLAY_MODE_DIAGNOSTIC:
		break;
	case _DISPLAY_MODE_OVERLAY:
		break;
	case _DISPLAY_MODE_SERVER:
		break;
	case _DISPLAY_MODE_CLIENT:
		break;
	case _DISPLAY_MODE_VARIABLE:
		break;
	default:
		break;

	}
}




// perform any necessary setup
void Display::init()
{
}
