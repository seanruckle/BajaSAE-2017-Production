#pragma once
#include <vector>
#include <fstream>
#include <cstdio>
#include <iostream>
#include "Variable.h"



class GetSetGenerator
{
public:
	GetSetGenerator();
	GetSetGenerator(const char* name);
	~GetSetGenerator();
	// Set the name of the source file.
	bool setSourceFile(const char* name);
	// Set the name of the output CPP file
	bool setOutputCPPFile(const char* name);
	// Set the name of the output H file
	bool setOutputHFile(const char * name);
	// Read contents of input file
	bool readInputFile();
	
	// calls generate functions inside loop, and performs higher order formatting operations
	bool generate();
	
	
private:
	// A place to put the variables
	std::vector<Variable> variableVector;

	// input file
	FILE* inputFile;
	std::string inputFileName;
	std::string outputHFileName;
	std::string outputCPPFileName;

	//std::string className;
	Variable classInfo;
	bool isClass;

	// Output File Stream
	std::ofstream outputHFile, outputCPPFile;

	// Get a line from the source file (Unimplemented)
	bool getLineFromSourceFile();


	// Generate class declaration
	bool generateClassDeclaration();
	bool generateClassEndBracket();
	bool generateClassComment();
	bool generateClassConstructorDeclaration();
	bool generateClassConstructorDefinition();

	bool generateClassHeaderInclude();

	bool generateVariableInitialization(Variable & variable);

	// Generate get function signature
	bool generateGetFunctionSignature(Variable & variable);


	// Generate set function signature
	bool generateSetFunctionSignature(Variable & variable);

	// Generate get function definition
	bool generateGetFunctionDefinition(Variable & variable);

	// Generate set function definition
	bool generateSetFunctionDefinition(Variable & variable);

	// Generate variable declarations
	bool generateVariableDeclaration(Variable & variable);
	
	// Generate variable comment
	bool generateVariableComment(Variable & variable);
};

