#pragma once
#include <string>
class Variable
{
public:
	Variable();
	~Variable();
	
	std::string type;
	std::string name;
	std::string value;
	std::string comment;
	

	//void operator=(Variable &source);

};

