// Smart Health Monitoring (Mock or real sensors)
// If you have MAX30102, DS18B20, etc., replace mock generators with real reads.
void setup(){
  Serial.begin(9600);
}
void loop(){
  // Mock vitals for demo
  int heart = 60 + random(0, 60);    // 60-120 bpm
  int spo2  = 94 + random(0, 6);     // 94-99 %
  float temp = 36.0 + (random(0, 80) / 10.0); // 36.0 - 44.0 C

  Serial.print("HR:"); Serial.print(heart);
  Serial.print(",SpO2:"); Serial.print(spo2);
  Serial.print(",Temp:"); Serial.println(temp);

  delay(1000);
}
