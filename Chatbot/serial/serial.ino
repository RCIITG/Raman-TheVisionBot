#include <Servo.h>

Servo ser;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ser.attach(11);
  ser.write(90);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available())
  {
    int in = Serial.read();
    Serial.println(in);
    ser.write(in);
  }
}
