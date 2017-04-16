#define _QUIET
#include "GetSetGenerator.h"
#include "Variable.h"
#include <iostream>

int main(int argc, char** argv) {
	if (argc < 2) {
		std::cout << "Ya dun goofed!\n\a";
		return -1;
	}

	for (int i = 1; i < argc; i++) {
		// the code generator object
		GetSetGenerator generator(argv[i]);

		generator.readInputFile();

		// Generate output
		if (generator.generate()) {
			std::cout << "Generation Fail" << std::endl;
		}

	}
	//std::getc(stdin);

	return 0;
}