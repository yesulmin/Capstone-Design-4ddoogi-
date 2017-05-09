#include <SoftwareSerial.h>

SoftwareSerial HM10(2,3); // RX, TX

void setup() {
  //기본 통신속도는 9600입니다.
  Serial.begin(9600);
  HM10.begin(9600);
}

void loop() {
  if (HM10.available()) {
    Serial.write(HM10.read());
  }
  if (Serial.available()) {
    HM10.write(Serial.read());
  }
}


