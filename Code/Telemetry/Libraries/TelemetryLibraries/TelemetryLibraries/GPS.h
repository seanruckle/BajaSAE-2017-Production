#pragma once

#include "State.h"
class GPS
{
public:
	GPS();
	~GPS();

	void getState(State& state);
};

