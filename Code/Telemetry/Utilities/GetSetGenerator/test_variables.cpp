#include "TestVar.h"

// Constructor for TestVar
TestVar::TestVar(){
	speed = 16;
	temp = 32;
	cowbell = 64;
	moreCowbell = 128;

}
// Set the value of speed
unsigned char TestVar::getSpeed() {
	return speed;
}
// Get the value of speed
void TestVar::setSpeed(unsigned char speed) {
	speed = this->speed;
}

// Set the value of temp
unsigned char TestVar::getTemp() {
	return temp;
}
// Get the value of temp
void TestVar::setTemp(unsigned char temp) {
	temp = this->temp;
}

// Set the value of cowbell
int TestVar::getCowbell() {
	return cowbell;
}
// Get the value of cowbell
void TestVar::setCowbell(int cowbell) {
	cowbell = this->cowbell;
}

// Set the value of moreCowbell
long int TestVar::getMoreCowbell() {
	return moreCowbell;
}
// Get the value of moreCowbell
void TestVar::setMoreCowbell(long int moreCowbell) {
	moreCowbell = this->moreCowbell;
}

