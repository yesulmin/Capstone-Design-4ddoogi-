#include <OneWire.h>  // 디지털 온도 센서를 사용하기 위해서는 이 라이브러리를 사용해야 한다.

OneWire ds(2); // 2번 핀에 연결된 OneWire 개체 생성

void setup() {
  Serial.begin(9600);
}

void loop() {
  byte i;
  byte present = 0;

  byte data[12];
  byte addr[8];
  float Temp;

  if (!ds.search(addr)) {
    ds.reset_search();
    return;
  }
  
  ds.reset();
  ds.select(addr);
  ds.write(0x44,1); // start conversion, with parasite power on at the end
  delay(1000);

  present = ds.reset();
  ds.select(addr);
  ds.write(0xBE); // Read Scratchpad

  for (i = 0; i < 9; i++) { // 센서에서 가져온 값을 정리하고 난 후 배열에 순서대로 넣어 둔다.
    data[i] = ds.read();
  }

  Temp=(data[1]<<8)+data[0];
  Temp=Temp/16;
  // 위에서 받아온 값중에 1번 배열에 있는 값을 256배(2의 8승) 해주고 0번 배열에 있는 값과 더해준다.
  // 그 값을 16으로 나누면 섭씨 온도가 된다.

  Serial.print("C=");
  Serial.print(Temp);
  Serial.print(", ");
  // 섭씨 출력

  Temp=Temp*1.8+32;
  // 섭씨를 화씨로 변환

  Serial.print("F=");
  Serial.print(Temp);
  Serial.println(" ");
  // 화씨 출력  
}
