#include <LiquidCrystal.h>

LiquidCrystal lcd(11, 10, 7, 6, 5, 4);

int dustPin=0;
float dustVal=0;
float dustDensity = 0;

int ledPower=2;
int delayTime=280;
int delayTime2=40;
float offTime=9680;

void setup(){
  lcd.begin(16, 2);
  lcd.print("  Dust density");
  
  Serial.begin(9600);
  pinMode(ledPower,OUTPUT);
  
}

void loop(){
  // ledPower is any digital pin on the arduino connected to Pin 3 on the sensor
  digitalWrite(ledPower,LOW); // power on the LED
  delayMicroseconds(delayTime);

  dustVal=analogRead(dustPin); // read the dust value via pin 5 on the sensor
  delayMicroseconds(delayTime2);

  digitalWrite(ledPower,HIGH); // turn the LED off
  delayMicroseconds(offTime);

  delay(1000);
    
    
  dustDensity = 0.17*dustVal;
  //Serial.print("Dust density(mg/m3) = ");
  lcd.setCursor(0, 1);
  lcd.print("     ");  
  lcd.print(dustDensity);  
  Serial.println(dustDensity);
  
}

