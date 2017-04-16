void clientEvent(Client client){
   input = client.readString(); 
   println(input, tmp);
   tmp++;
}
void serialEvent(Serial a){
  inBuffer = myPort.readStringUntil('#');
  if(inBuffer != null){
    inBuffer = inBuffer.substring(0,inBuffer.length()-1);
    client.write(inBuffer);
    println(inBuffer);
    println(tmp);
    tmp++;
  }
}