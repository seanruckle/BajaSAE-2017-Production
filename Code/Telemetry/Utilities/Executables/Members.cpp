#include "Member.h"

// Constructor for Member
Member::Member(){
	name = "Ash";
	subteam = 'E';
	CPlusPlus = FALSE;
	AVR = FALSE;
	Arduino = FALSE;
	Linux = FALSE;
	GUI = FALSE;
	Python = FALSE;
	Java = FALSE;
	HTML = FALSE;
	CSS = FALSE;
	JavaScript = FALSE;
	Csharp = FALSE;
	Eagle = FALSE;
	DesignSpark = FALSE;
	SolidWorks = FALSE;
	Printing3D = FALSE;
	Circuit Design = FALSE;
	PCBLayout = FALSE;
	GraphicDesing = FALSE;
	ServerAdministration = FALSE;
	FEA = FALSE;
	GearboxDesign = FALSE;
	Welding = FALSE;
	Soldering = FALSE;
	C = FALSE;
	Datasheets = FALSE;
	Googling = FALSE;
	StyleGuides = FALSE;
	Git = FALSE;
	MachineShopAccess = FALSE;

}
// Set the value of name
std::string Member::getName() {
	return name;
}
// Get the value of name
void Member::setName(std::string name) {
	name = this->name;
}

// Set the value of subteam
char Member::getSubteam() {
	return subteam;
}
// Get the value of subteam
void Member::setSubteam(char subteam) {
	subteam = this->subteam;
}

// Set the value of CPlusPlus
bool Member::getCPlusPlus() {
	return CPlusPlus;
}
// Get the value of CPlusPlus
void Member::setCPlusPlus(bool CPlusPlus) {
	CPlusPlus = this->CPlusPlus;
}

// Set the value of AVR
bool Member::getAVR() {
	return AVR;
}
// Get the value of AVR
void Member::setAVR(bool AVR) {
	AVR = this->AVR;
}

// Set the value of Arduino
bool Member::getArduino() {
	return Arduino;
}
// Get the value of Arduino
void Member::setArduino(bool Arduino) {
	Arduino = this->Arduino;
}

// Set the value of Linux
bool Member::getLinux() {
	return Linux;
}
// Get the value of Linux
void Member::setLinux(bool Linux) {
	Linux = this->Linux;
}

// Set the value of GUI
bool Member::getGUI() {
	return GUI;
}
// Get the value of GUI
void Member::setGUI(bool GUI) {
	GUI = this->GUI;
}

// Set the value of Python
bool Member::getPython() {
	return Python;
}
// Get the value of Python
void Member::setPython(bool Python) {
	Python = this->Python;
}

// Set the value of Java
bool Member::getJava() {
	return Java;
}
// Get the value of Java
void Member::setJava(bool Java) {
	Java = this->Java;
}

// Set the value of HTML
bool Member::getHTML() {
	return HTML;
}
// Get the value of HTML
void Member::setHTML(bool HTML) {
	HTML = this->HTML;
}

// Set the value of CSS
bool Member::getCSS() {
	return CSS;
}
// Get the value of CSS
void Member::setCSS(bool CSS) {
	CSS = this->CSS;
}

// Set the value of JavaScript
bool Member::getJavaScript() {
	return JavaScript;
}
// Get the value of JavaScript
void Member::setJavaScript(bool JavaScript) {
	JavaScript = this->JavaScript;
}

// Set the value of Csharp
bool Member::getCsharp() {
	return Csharp;
}
// Get the value of Csharp
void Member::setCsharp(bool Csharp) {
	Csharp = this->Csharp;
}

// Set the value of Eagle
bool Member::getEagle() {
	return Eagle;
}
// Get the value of Eagle
void Member::setEagle(bool Eagle) {
	Eagle = this->Eagle;
}

// Set the value of DesignSpark
bool Member::getDesignSpark() {
	return DesignSpark;
}
// Get the value of DesignSpark
void Member::setDesignSpark(bool DesignSpark) {
	DesignSpark = this->DesignSpark;
}

// Set the value of SolidWorks
bool Member::getSolidWorks() {
	return SolidWorks;
}
// Get the value of SolidWorks
void Member::setSolidWorks(bool SolidWorks) {
	SolidWorks = this->SolidWorks;
}

// Set the value of Printing3D
bool Member::getPrinting3D() {
	return Printing3D;
}
// Get the value of Printing3D
void Member::setPrinting3D(bool Printing3D) {
	Printing3D = this->Printing3D;
}

// Set the value of Circuit Design
bool Member::getCircuit Design() {
	return Circuit Design;
}
// Get the value of Circuit Design
void Member::setCircuit Design(bool Circuit Design) {
	Circuit Design = this->Circuit Design;
}

// Set the value of PCBLayout
bool Member::getPCBLayout() {
	return PCBLayout;
}
// Get the value of PCBLayout
void Member::setPCBLayout(bool PCBLayout) {
	PCBLayout = this->PCBLayout;
}

// Set the value of GraphicDesing
bool Member::getGraphicDesing() {
	return GraphicDesing;
}
// Get the value of GraphicDesing
void Member::setGraphicDesing(bool GraphicDesing) {
	GraphicDesing = this->GraphicDesing;
}

// Set the value of ServerAdministration
bool Member::getServerAdministration() {
	return ServerAdministration;
}
// Get the value of ServerAdministration
void Member::setServerAdministration(bool ServerAdministration) {
	ServerAdministration = this->ServerAdministration;
}

// Set the value of FEA
bool Member::getFEA() {
	return FEA;
}
// Get the value of FEA
void Member::setFEA(bool FEA) {
	FEA = this->FEA;
}

// Set the value of GearboxDesign
bool Member::getGearboxDesign() {
	return GearboxDesign;
}
// Get the value of GearboxDesign
void Member::setGearboxDesign(bool GearboxDesign) {
	GearboxDesign = this->GearboxDesign;
}

// Set the value of Welding
bool Member::getWelding() {
	return Welding;
}
// Get the value of Welding
void Member::setWelding(bool Welding) {
	Welding = this->Welding;
}

// Set the value of Soldering
bool Member::getSoldering() {
	return Soldering;
}
// Get the value of Soldering
void Member::setSoldering(bool Soldering) {
	Soldering = this->Soldering;
}

// Set the value of C
bool Member::getC() {
	return C;
}
// Get the value of C
void Member::setC(bool C) {
	C = this->C;
}

// Set the value of Datasheets
bool Member::getDatasheets() {
	return Datasheets;
}
// Get the value of Datasheets
void Member::setDatasheets(bool Datasheets) {
	Datasheets = this->Datasheets;
}

// Set the value of Googling
bool Member::getGoogling() {
	return Googling;
}
// Get the value of Googling
void Member::setGoogling(bool Googling) {
	Googling = this->Googling;
}

// Set the value of StyleGuides
bool Member::getStyleGuides() {
	return StyleGuides;
}
// Get the value of StyleGuides
void Member::setStyleGuides(bool StyleGuides) {
	StyleGuides = this->StyleGuides;
}

// Set the value of Git
bool Member::getGit() {
	return Git;
}
// Get the value of Git
void Member::setGit(bool Git) {
	Git = this->Git;
}

// Set the value of MachineShopAccess
bool Member::getMachineShopAccess() {
	return MachineShopAccess;
}
// Get the value of MachineShopAccess
void Member::setMachineShopAccess(bool MachineShopAccess) {
	MachineShopAccess = this->MachineShopAccess;
}

