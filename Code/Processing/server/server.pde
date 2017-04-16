import processing.net.*;

String carIP = ("192.168.2.5"); //cars ip adress

Server server; 
Client client;
Client car = null;

communicationClass com;
String input;
String data[];
int tmp = 0;


void setup() { 
  size(720,480);
  //fullScreen();
  background(204);
  server = new Server(this, 12345);  // Start a simple server on a port  
} 

void draw() { 
  com.receiveData();  
}