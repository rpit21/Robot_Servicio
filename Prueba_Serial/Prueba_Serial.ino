String cad;

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(9600);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial1.available()){
    cad=Serial1.readStringUntil('\n');
    Serial.print("Dato:");
    Serial.println(cad);
  }

  //Serial.print("Sin dato");
}
