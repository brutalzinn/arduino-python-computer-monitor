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
int Li          = 16;
int Lii         = 0; 
int Ri          = -1;
int Rii         = -1;
byte inData;
char inChar;
String BuildINString = "";
char c = "";

boolean NL = true;
String txtsc,txtnosc;

void setup()
{
  lcd.init();                      // initialize the lcd
  lcd.backlight();
  lcd.clear();
  Serial.begin(9600);
}
String Scroll_LCD_Left(String StrDisplay){
  String result;
  String StrProcess = "                " + StrDisplay + "                ";
  result = StrProcess.substring(Li,Lii);
  Li++;
  Lii++;
  if (Li>StrProcess.length()){
    Li=16;
    Lii=0;
  }
  return result;
}
void loop()
{

  //This part accumulates the characters from the HC05 TX in a serial fasion and concats a string(BuildINstring) out of them
  //  BuildINString = "";
  // when characters arrive over the serial port...
  int size_ = 0;
  String  payload;
  if (Serial.available()) {
    while (Serial.available()) {
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
      lcd.print(Scroll_LCD_Left(mem));
      lcd.setCursor(0, 1);
      lcd.print("PROC:");
      delay(500);

      Serial.flush();
      // lcd.print(" ");
      // lcd.print((char)223);
      // lcd.print("C");

    }
  }
}
String ScrollTxt(String txt) {
  return txt.substring(1, txt.length()) + txt.substring(0, 1);
}
