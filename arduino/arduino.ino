
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

LiquidCrystal_I2C lcd(0x3F, 16, 2); // set the LCD address to 0x27 for a 16 chars and 2 line display
int Li          = 16;
int Lii         = 0;
int Ri          = -1;
int Rii         = -1;
int memInputIndicator = 7;
boolean statusConnected = false;
String rowone = "";
String rowtwo = "";
boolean maxMem = false;
void setup()
{
  lcd.init();                      // initialize the lcd
  lcd.backlight();
  pinMode(memInputIndicator, OUTPUT);
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
void checkMaxMem() {
  if (maxMem) {
    digitalWrite(memInputIndicator, HIGH);
  } else {
    digitalWrite(memInputIndicator, LOW);
  }
}
void loop()
{

  //lcd.clear();
  if (Serial.available()) {

    StaticJsonDocument<256> doc;
    JsonObject root = doc.to<JsonObject>();


    DeserializationError err = deserializeJson(doc, Serial);
    if (err) {
      Serial.println("ERRROR");
      Serial.flush();
      return;
    }
    if (!statusConnected) {
      String status = doc["status"];
      if (status == "1") {
        statusConnected = true;
        Serial.println("1");
      } else {
        statusConnected = false;
      }

    }

    bool hasRowOne = root.containsKey("rowone");
    bool hasRowTwo = root.containsKey("rowtwo");
    bool hasMaxMem = root.containsKey("maxmem");

    if (hasRowOne) {
      rowone = doc["rowone"].as<String>();
    }
    if (hasRowTwo) {
      rowtwo = doc["rowtwo"].as<String>();
    }
    if (hasMaxMem) {
      String maxMemTest = doc["maxmem"].as<String>();
      if(maxMemTest == "1"){
        maxMem = true;
      }else{
        maxMem = false;
      }
      checkMaxMem();
    }
  }
  lcd.setCursor(0, 0);
  lcd.print(rowone);
  lcd.setCursor(0, 1);
  lcd.print(rowtwo);
 
}
