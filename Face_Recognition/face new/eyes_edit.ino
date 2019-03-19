#include <Servo.h>
// define parameters
// input value between 0-255
int in;
// head initial value
int prev1 = 90;
// eye inital value
int prev2 = 90;
//degree of rotation
int i = 2;

Servo head;
Servo eyes;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // attach head to pin 9
  head.attach(9);
  // attach eyes to pin 11
  eyes.attach(11);
  // initialize head
  head.write(prev1);
  // initialize eyes
  eyes.write(prev2);
  
  }

void loop() {
  // if Serial input is available
  if (Serial.available()){
    //Read input
    in = Serial.read();
    Serial.println(in);
    //If input is 255 then make a sweep
    if (in == 255){
      for (prev1 = 90; prev1 >=20; prev1 -= 1){
        head.write(prev1);
        delay(50);
        if (Serial.available() && in <=254){
          break;
          }
        }
      for (prev1; prev1 <= 160; prev1 += 1) {
        head.write(prev1);
        delay(50);
        if (Serial.available() && in <=254){
          break;
          }
        }
       for (prev1; prev1>= 20; prev1 -= 1) {
        head.write(prev1);
        delay(50);
        if (Serial.available() && in <=254){
          break;
          }
        }
        for (prev1; prev1<= 90; prev1 += 1) {
        head.write(prev1);
        delay(50);
        if (Serial.available() && in <=254){
          break;
          }
        }
      }
    //move left if input is more than threshold of 180
    if (in>180){
      prev1 = prev1 - i;
      head.write(prev1);
      delay(50);
      
      if (prev2<90) {
        prev2 = prev2 + i;
        eyes.write(prev2);
        delay(5);
      }
      else {
        prev2 = prev2 - i;
        eyes.write(prev2);
        delay(5);
        }
    }
    // move right if input is less than threshold of 80    
    else if (in<80){
      prev1 = prev1 + i;
      head.write(prev1);
      delay(50);
      if (prev2<90) {
        prev2 = prev2 + i;
        eyes.write(prev2);
        delay(5);
      }
      else {
        prev2 = prev2 - i;
        eyes.write(prev2);
        delay(5);
        }
      }

      
      
    if (prev2<90) {
      prev2 = prev2 + i;
      eyes.write(prev2);
      delay(5);
    }
    else {
      prev2 = prev2 - i;
      eyes.write(prev2);
      delay(5);
      }

    // similar to above thresholds make thresholds for eyes
    if (in<105){
      prev2 = 75;
      eyes.write(prev2);
      }
    else if (in>150){
      prev2 = 105;
      eyes.write(prev2);
      }
    }
  }
