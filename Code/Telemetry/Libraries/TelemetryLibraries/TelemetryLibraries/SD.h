#pragma once
#include <string>
#include "State.h"
class SD
{
public:
	SD();
	~SD();

	void writeString(std::string data);
	void writeState(State & state);
};

