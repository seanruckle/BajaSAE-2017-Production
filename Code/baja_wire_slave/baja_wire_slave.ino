#include <Wire.h>
int data;
int datalen;
bool authenticate;
int myAddress;
int len;
int master=0;
void setup() {
  // put your setup code here, to run once:
Wire.begin(1);
Wire.setClock(100000);
sensor_calibration();
}

void loop() {
  // put your main code here, to run repeatedly:
Wire.onReceive(Authentication);
sensor_shit();

}

void Authentication(){
//send buffer and stop
authenticate=Wire.read();
if (authenticate==true){
Wire.beginTransmission(master);
Wire.write(myAddress);
Wire.write(data);
Wire.endTransmission();
}
 

}
void sensor_shit(){
  
}

void sensor_calibration(){
  
}

