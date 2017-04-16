void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("hello world#");
  delay(500);        // delay in between reads for stability
}
