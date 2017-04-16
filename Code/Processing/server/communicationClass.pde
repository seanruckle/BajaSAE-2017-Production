class communicationClass{
boolean receiveData(){
  client = server.available();
  if (client != null) {
    input = client.readString(); 
    println(input, tmp);
    tmp++;
    return true;
  }
  else{
    return false;
  }
}
boolean writeCar(String data){
  if(car != null){
    car.write(data);
    return true;
  }
  return false;
}

}