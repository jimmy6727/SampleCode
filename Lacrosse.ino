#include "LCD.h"
#include "Menu.h"
#include "Led.h"
#include "Keypad.h"
#include "Motor.h"
#include "ArmControl.h"
#include "WTV020SD16P.h"
#include "OLEDDisplay.h"
#include "SSD1306.h"


void setup()
 {
  Serial.begin(115200);
  LCD_init();
  Serial.println("OK");
  LCD_addStr(20,0,TEXT_MEDIUM,"Init v0.2.2");
  Menu_init();
  Keypad_init();
  Led_init();
  Motor_init();
  Solenoid_init();
  Arm_init();
}

void loop()
{
  LCD_process ();
  Keypad_process();
  Menu_process();
  //userRequestHandler();
}
