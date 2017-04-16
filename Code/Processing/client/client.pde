import processing.net.*; 
import processing.serial.*;

String IP = "192.168.2.4"; //Server IP address

Client client; 
Serial myPort;  // The serial port

String input;
int data[]; 
int tmp;
String inBuffer;

void setup() { 
  size(720,480);
  background(204);
  client = new Client(this, IP, 12345); // Replace with your server’s IP and port
  printArray(Serial.list());
  // Open the port you are using at the rate you want:
  myPort = new Serial(this, Serial.list()[0], 9600);
  myPort.bufferUntil('#');
} 

void draw() {   

}