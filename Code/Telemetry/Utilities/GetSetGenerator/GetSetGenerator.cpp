#include "GetSetGenerator.h"
//#define _DEBUG_MODE_ENABLED
// For use in input state machine
#define READING_TYPE 01
#define READING_NAME 02
#define READING_VALUE 03
#define READING_COMMENT 04

#define _QUIET


GetSetGenerator::GetSetGenerator()
{
}

GetSetGenerator::GetSetGenerator(const char * name)
{
	// Store name of input file
	inputFileName.assign(name);
	outputCPPFileName.assign(name);
	outputHFileName.assign(name);

#ifdef _DEBUG_MODE_ENABLED
	std::cout << "Position of last '.': " << inputFileName.find_last_of('.') << "\n";
	std::cout << "Length of string: " << inputFileName.size() << "\n";
	std::cout << "Difference: " << (inputFileName.size() - inputFileName.find_last_of('.')) << "\n";
#endif

	size_t fileNameLength = inputFileName.size();
	size_t lastPeriodIndex = inputFileName.find_last_of('.');
	bool hasExtension = ((fileNameLength - lastPeriodIndex) <= 4) && ((fileNameLength - lastPeriodIndex) > 0);
	// Change file extension for output CPP file
	if (hasExtension) {
		outputCPPFileName.erase(outputCPPFileName.find_last_of('.'));
	}
	outputCPPFileName.append(".cpp");

	// Change file extension for output H file
	if (hasExtension) {
		outputHFileName.erase(outputHFileName.find_last_of('.'));
	}
	outputHFileName.append(".h");

	setSourceFile(inputFileName.c_str());
	setOutputCPPFile(outputCPPFileName.c_str());
	setOutputHFile(outputHFileName.c_str());
}


GetSetGenerator::~GetSetGenerator()
{
	fclose(inputFile);
	outputCPPFile.close();
	outputHFile.close();
	variableVector.clear();
}


// Set the name of the source file.
bool GetSetGenerator::setSourceFile(const char* name)
{
	if (name) {	// If the name is not blank
		inputFile = fopen(name, "r");		// Open input file
		if (inputFile != NULL) {			// Check that the file was successfully opened
			return false;					// Return no Error
		}
	}
	return true;						// Return Error
}


// Set the name of the output CPP file
bool GetSetGenerator::setOutputCPPFile(const char* name)
{
	if (name) {	// If the name is not blank
		outputCPPFile.open(name);			// Open output CPP file
		if (outputCPPFile.is_open()) {		// Check that the file is actually opened
			return false;					// Return no Error
		}
	}
	return true;						// Return Error
}


bool GetSetGenerator::setOutputHFile(const char* name)
{
	if (name) {	// If the name is not blank
		outputHFile.open(name);			// Open output CPP file
		if (outputHFile.is_open()) {		// Check that the file is actually opened
			return false;					// Return no Error
		}
	}
	return true;						// Return Error
}

bool GetSetGenerator::readInputFile() {
	char c = '\0';	// Initialize to null character

	bool variableExists = false;
	bool endOfFile = false;
	int column = READING_TYPE;

#ifndef _QUIET
	// Print Diagnostic Information
	std::cout << "Start Reading " << inputFileName.substr(inputFileName.find_last_of('\\') + 1) << "\n";
#endif
	Variable tempVariable;
	do {
		fscanf(inputFile, "%c", &c);
		// TODO: replace with state machine
		switch (c) {
		case EOF:
			// check for errors then return
			endOfFile = true;
			break;
		case ',':
			// React differently based on mode
			switch (column) {
			case READING_TYPE:
				// now reading variable name
				column = READING_NAME;
				break;
			case READING_NAME:
				// now reading variable comment
				column = READING_VALUE;
				break;
			case READING_VALUE:
				column = READING_COMMENT;
				break;
			case READING_COMMENT:
				if (variableExists) {			// Can't have just a comment
					tempVariable.comment += c;	// Append to comment string
				}
				// treat as any other character
				break;
			}
			break;
		case '\n':
			// Move to next variable
			if (!variableExists) {
				break;
			}
			variableExists = false;
			column = READING_TYPE;
			variableVector.push_back(tempVariable); // Add variable to vector
			tempVariable.name.clear();
			tempVariable.type.clear();
			tempVariable.value.clear();
			tempVariable.comment.clear();

			break;
		default:
			// reading some character
			if (!variableExists) {
				// Clear the contents of the temp variable
				tempVariable.name.clear();
				tempVariable.type.clear();
				tempVariable.value.clear();
				tempVariable.comment.clear();
				variableExists = true;
			}

			switch (column) {
			case READING_TYPE:
				tempVariable.type += c;		// Append to type string
				break;
			case READING_NAME:
				tempVariable.name += c;		// Append to name string
				break;
			case READING_VALUE:
				tempVariable.value += c;
				break;
			case READING_COMMENT:
				tempVariable.comment += c;	// Append to comment string
				break;
			}

			break;
		}
		if (endOfFile) {	// We are done here...
			break;
		}
	} while (!feof(inputFile));
#ifndef _QUIET
	// Print Diagnostic Information
	std::cout << "Finished Reading " << inputFileName.substr(inputFileName.find_last_of('\\') + 1) << "\n";
#endif
	return false;
}
// calls generate functions inside loop, and performs higher order formatting operations
bool GetSetGenerator::generate()
{
	if (variableVector.size() <= 0) {
		return true;
	}

	if (!(variableVector.front().type.compare("class"))) {
		//className = variableVector.front().name;
		classInfo = variableVector.front();
		variableVector.erase(variableVector.begin());
		isClass = true;
#ifndef _QUIET
		// Print Diagnostic Information
		std::cout << "Class Found in " << inputFileName.substr(inputFileName.find_last_of('\\') + 1) << "\n";
#endif
	}
	else {
		isClass = false;
	}

	if (isClass) {		// Only do this if it is a class. Otherwise just generate the code.
#ifndef _QUIET
						// Print Diagnostic Information
		std::cout << "Printing Class Declaration to " << outputHFileName.substr(outputHFileName.find_last_of('\\') + 1) << "\n";
#endif
		generateClassComment();
		generateClassDeclaration();
		outputHFile << "public:" << "\n" << "\n";
		generateClassConstructorDeclaration();
		outputHFile << "private:" << "\n" << "\n";
#ifndef _QUIET
		// Print Diagnostic Information
		std::cout << "Printing header #include and Constructor to " << outputHFileName.substr(outputHFileName.find_last_of('\\') + 1) << "\n";
#endif
		generateClassHeaderInclude();
		generateClassConstructorDefinition();
	}


#ifndef _QUIET
	// Print Diagnostic Information
	std::cout << "Writing Private Members to " << outputHFileName.substr(outputHFileName.find_last_of('\\') + 1) << "\n";
#endif

	// Loop through variable Vector generating private members
	for (Variable &variableReference : variableVector) {
		generateVariableComment(variableReference);
		if (generateVariableDeclaration(variableReference)) {
			return true;
		}
	}
	outputHFile << "\n";

	if (isClass) {		// Only do this if it is a class. Otherwise just generate the code.
		outputHFile << "public:" << "\n" << "\n";
	}

#ifndef _QUIET
	// Print Diagnostic Information
	std::cout << "Writing Public Members to " << outputHFileName.substr(outputHFileName.find_last_of('\\') + 1) << " and " << outputCPPFileName.substr(outputCPPFileName.find_last_of('\\') + 1) << "\n";
#endif

	// Loop through variable vector generating public members
	for (Variable &variableReference : variableVector) {

		generateGetFunctionSignature(variableReference);
		generateSetFunctionSignature(variableReference);
		outputHFile << "\n";

		generateGetFunctionDefinition(variableReference);
		generateSetFunctionDefinition(variableReference);
		outputCPPFile << "\n";

	}

	if (isClass) {		// Only do this if it is a class. Otherwise just generate the code.
		generateClassEndBracket();
	}

#ifndef _QUIET
	// Print Diagnostic Information
	std::cout << "Finished Writing to " << outputHFileName.substr(outputHFileName.find_last_of('\\') + 1) << " and " << outputCPPFileName.substr(outputCPPFileName.find_last_of('\\') + 1) << "\n";
#endif

	return false;
}

// Deprecated
bool GetSetGenerator::getLineFromSourceFile()
{
	return true;
}

bool GetSetGenerator::generateClassDeclaration()
{
	outputHFile << "class " << classInfo.name << "{ " << "\n";
	return false;
}

bool GetSetGenerator::generateClassEndBracket()
{
	outputHFile << "\n" << "};";
	return false;
}

bool GetSetGenerator::generateClassComment()
{

	if (classInfo.comment.size()) {
		outputHFile << "/* " << "\n";
		outputHFile << classInfo.comment.c_str() << "\n";
		outputHFile << "*/" << "\n";
	}

	return false;
}

bool GetSetGenerator::generateClassConstructorDeclaration()
{
	outputHFile << "// Constructor for " << classInfo.name << "\n";
	outputHFile << classInfo.name << "();" << "\n";
	return false;
}

bool GetSetGenerator::generateClassConstructorDefinition()
{
	outputCPPFile << "// Constructor for " << classInfo.name << "\n";
	outputCPPFile << classInfo.name << "::" << classInfo.name << "(){" << "\n";
	for (Variable &variableReference : variableVector) {
		generateVariableInitialization(variableReference);
	}
	outputCPPFile << "\n}\n";
	
	return false;
}

bool GetSetGenerator::generateClassHeaderInclude()
{
	outputCPPFile << "#include \"" << classInfo.name << ".h\"" << "\n\n";
	return false;
}

bool GetSetGenerator::generateVariableInitialization(Variable & variable) {
	
	outputCPPFile << "\t" << variable.name << " = " << variable.value << ";\n";
	return false;
}

bool GetSetGenerator::generateGetFunctionSignature(Variable& variable)
{
	// Create a temporary string with the upper case initial version of the variable name
	char tempName[50];
	std::strcpy(tempName, variable.name.c_str());
	tempName[0] = toupper(tempName[0]);

	outputHFile << "// Get the value of " << variable.name << "\n";			// This line creates a standard comment describing what the generated function does
	outputHFile << variable.type << " get" << tempName << "();" << "\n";	// type getName();\n
	return false;
}

bool GetSetGenerator::generateSetFunctionSignature(Variable & variable)
{
	// Create a temporary string with the upper case initial version of the variable name
	char tempName[50];
	std::strcpy(tempName, variable.name.c_str());
	tempName[0] = toupper(tempName[0]);

	outputHFile << "// Set the value of " << variable.name << "\n";			// This line creates a standard comment describing what the generated function does
	outputHFile << "void set" << tempName << "(" << variable.type.c_str() << " " << variable.name << ");" << "\n";	// void setName(type name);\n
	return false;
}


bool GetSetGenerator::generateGetFunctionDefinition(Variable & variable)
{
	// Create a temporary string with the upper case initial version of the variable name
	char tempName[50];
	std::strcpy(tempName, variable.name.c_str());
	tempName[0] = toupper(tempName[0]);

	outputCPPFile << "// Set the value of " << variable.name.c_str() << "\n";			// This line creates a standard comment describing what the generated function does
	outputCPPFile << variable.type.c_str() << " ";
	if (isClass) {
		outputCPPFile << classInfo.name << "::";
	}
	outputCPPFile << "get" << tempName << "() {" << "\n";	// type getName() {\n
	outputCPPFile << "\treturn " << variable.name.c_str() << ";" << "\n";					//		return this->name;\n
	outputCPPFile << "}" << "\n";																	// }\n
	return false;
}

bool GetSetGenerator::generateSetFunctionDefinition(Variable & variable)
{
	// Create a temporary string with the upper case initial version of the variable name
	char tempName[50];
	std::strcpy(tempName, variable.name.c_str());
	tempName[0] = toupper(tempName[0]);

	outputCPPFile << "// Get the value of " << variable.name.c_str() << "\n";		// This line creates a standard comment describing what the generated function does
	outputCPPFile << "void ";
	if (isClass) {
		outputCPPFile << classInfo.name << "::";
	}
	outputCPPFile << "set" << tempName << "(" << variable.type.c_str() << " " << variable.name.c_str() << ") {" << "\n";	// void setName(type name) {\n
	outputCPPFile << "\t" << variable.name.c_str() << " = this->" << variable.name.c_str() << ";" << "\n";					//		return this->name;\n
	outputCPPFile << "}" << "\n";
	return false;
}
// Generate variable declarations
bool GetSetGenerator::generateVariableDeclaration(Variable & variable)
{
	// Create a temporary string with the upper case initial version of the variable name
	char tempName[50];
	std::strcpy(tempName, variable.name.c_str());
	tempName[0] = toupper(tempName[0]);

	//outputHFile << "\n";
	outputHFile << variable.type << " " << variable.name << ";" << "\n";	// type name;\n
	return false;
}

bool GetSetGenerator::generateVariableComment(Variable & variable)
{
	if (variable.comment.size()) {
		outputHFile << "/* ";
		outputHFile << variable.comment;
		outputHFile << " */" << "\n";

	}
	return false;
}


