#include <DHT.h>

DHT sensor(8,DHT11);
float temp;

void setup() {
  Serial.begin(9600);
  sensor.begin();
}

void loop() {
  while(!Serial.available());
  if(Serial.read()=='A') {
    temp = sensor.readTemperature();
    if(isnan(temp)) Serial.print("ERROR");
    else Serial.print(temp);
  }
}
