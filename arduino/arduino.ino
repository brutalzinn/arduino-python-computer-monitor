/*
   Displays text sent over the serial port (e.g. from the Serial Monitor) on
   an attached LCD.
   YWROBOT
  Compatible with the Arduino IDE 1.0
  Library version:1.1
*/
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

LiquidCrystal_I2C lcd(0x3F, 16, 2); // set the LCD address to 0x27 for a 16 chars and 2 line display
byte inData;
char inChar;
String BuildINString = "";
char c = "";

boolean NL = true;
void setup()
{
  lcd.init();                      // initialize the lcd
  lcd.backlight();
  lcd.clear();
  Serial.begin(9600);
}

void loop()
{

  //This part accumulates the characters from the HC05 TX in a serial fasion and concats a string(BuildINstring) out of them
  //  BuildINString = "";
  // when characters arrive over the serial port...
  int size_ = 0;
  String  payload;
  while (Serial.available()) {
    delay(100);
    lcd.clear();
    payload = Serial.readStringUntil( '\n' );
    StaticJsonDocument<512> doc;

    DeserializationError err = deserializeJson(doc, payload);
    if (err) {
      Serial.flush();
      return;
    }
    String mem = doc["mem"];
    lcd.setCursor(0, 0);
    lcd.print("MEM:");
    lcd.print(mem);
    lcd.setCursor(0, 1);
    lcd.print("PROC:");
    Serial.flush();
    // lcd.print(" ");
    // lcd.print((char)223);
    // lcd.print("C");


  }
}
