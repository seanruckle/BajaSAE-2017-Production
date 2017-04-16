void serverEvent(Server someServer, Client someClient) {
  if(someClient.ip() == carIP){
    car = someClient;
  }  
}
void keyPressed(){
  println("pressed");
}