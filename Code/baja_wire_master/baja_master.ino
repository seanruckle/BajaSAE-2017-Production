#include <Wire.h>
#include <String.h>
int data;
bool authenticate=true;
int address;
void setup() {
  // put your setup code here, to run once:
Wire.begin(0);
Wire.setClock(100000);
}

void loop() {
  // put your main code here, to run repeatedly:
ask(address, authenticate);
Wire.onReceive(organize);

}
void handler(){
  while (1<Wire.available()){
    data=Wire.read();
  }
  
}
void ask(int address, bool authenticate){
Wire.beginTransmission(address);//(address)change address here based on slave
Wire.write(authenticate);
Wire.endTransmission();

}

void organize(){
  for (int i=0;1<Wire.available();i++){
    data=Wire.read();
  }
}



