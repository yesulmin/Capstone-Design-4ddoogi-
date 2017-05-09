void setup() 
{   Serial.begin(9600); }
void loop()
{ char pr[12];
  sprintf(pr, "Light = %d", analogRead(A0));
  Serial.println(pr);
  delay(100);     // sprintf 함수 예제 출력 테스트
}

