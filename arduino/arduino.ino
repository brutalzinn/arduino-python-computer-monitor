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
boolean statusConnected = false;
String rowone = "";
String rowtwo = "";

void setup()
{
  lcd.init();                      // initialize the lcd
  lcd.backlight();
  Serial.begin(9600);
}
String Scroll_LCD_Left(String StrDisplay) {
  String result;
  String StrProcess = "                " + StrDisplay + "                ";
  result = StrProcess.substring(Li, Lii);
  Li++;
  Lii++;
  if (Li > StrProcess.length()) {
    Li = 16;
    Lii = 0;
  }
  return result;
}
void loop()
{

  //lcd.clear();
  while (Serial.available()) {

    StaticJsonDocument<1024> doc;


    DeserializationError err = deserializeJson(doc, Serial);
    if (err) {
      Serial.flush();
      return;
    }
    String status = doc["status"].as<String>();
    if (status == "1") {
      statusConnected = true;
      Serial.println("1");
    } else {
      statusConnected = false;
      // Serial.println("0");
    }
   if(!statusConnected){
    return;
   }
     rowone = doc["rowone"].as<String>();
   
     rowtwo = doc["rowtwo"].as<String>();
  }
  lcd.setCursor(0, 0);
  lcd.print(Scroll_LCD_Left(rowone));
  lcd.setCursor(0, 1);
  lcd.print(Scroll_LCD_Left(rowtwo));
  delay(1000);
  Serial.flush();


}
String ScrollTxt(String txt) {
  return txt.substring(1, txt.length()) + txt.substring(0, 1);
}
