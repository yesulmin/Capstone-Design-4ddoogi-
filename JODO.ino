void setup() 
{   Serial.begin(9600); }
void loop()
{ char pr[12];
  sprintf(pr, "Light = %d", analogRead(A0));
  Serial.println(pr);
  delay(100);     // sprintf 함수 예제 출력 테스트
}

//10 LUX -> 20~30KOhm
//Lux++ -> Ohm--
//Error value is too high.

//int analogV = analogRead(A0);         //0-1023
//float V = arduVolt*analogV/(1023.0);  //1K옴 저항 전압 환산
//float i = V/r;                        //1K옴 저항 전류 계산, 암페어 
//float cdsV = arduVolt-V;              //조도센서 전압 계산 
//float cdsR = cdsV/i;                  //조도센서 저항 계산 
//float cdsRk=cdsR/1000.0;              //k옴으로 환산
