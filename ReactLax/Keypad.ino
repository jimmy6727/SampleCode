#include "Keypad.h"



#ifdef  KEYPAD_DEBUG
#define Keypad_debugPrintf(...) Serial.printf(__VA_ARGS__);
#else
#define Keypad_debugPrintf(...);
#endif

static Button_t pressedButton;
static bool s_isPresed;
static uint16_t s_kButtonValueDeadZone = 15;

enum KeypadState {k_KeypadWait, k_KeypadPressed, k_KeypadReleaseWait, k_KeypadBounceWait};

const uint16_t s_kButtonsValues[12] = {460, 1023, 935, 815, 735,  677,
                                       628, 586,  549, 517, 485,  436};

/*const uint16_t s_kButtonsValues[12] = {465, 1010, 940, 820, 720,  670,
                                       630, 592, 552, 507, 424};*/
                                       
void Keypad_init()
{
  s_isPresed = false;
  pressedButton = k_buttonNone;
  pinMode(KEYPAD_PIN, INPUT);
  analogSetWidth(10);
}

// Keypad button logic
void Keypad_process()
{
  static uint8_t s_keypadState = k_KeypadWait;
  static uint32_t s_buttonBounceTime = 0;
  const uint16_t l_kButtonBounseDelay = 300;
  uint16_t l_val = analogRead(KEYPAD_PIN);
  switch (s_keypadState){
    case k_KeypadWait:
      if (l_val > 100){
        s_keypadState = k_KeypadPressed;
      }
      break;
    case k_KeypadPressed:
       Keypad_debugPrintf("keypad batton val %d\n", l_val);
      if ((s_kButtonsValues[7] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[7] < (l_val + s_kButtonValueDeadZone))){
        Keypad_debugPrintf("Pressed button Up\n");
        pressedButton = k_buttonUp;
      }
      if ((s_kButtonsValues[8] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[8] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonSet;//k_buttonDown;
        Keypad_debugPrintf("Pressed button Set\n");
      }
      if ((s_kButtonsValues[0] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[0] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonLeft;
        Keypad_debugPrintf("Pressed button Left\n");
      }
      if ((s_kButtonsValues[5] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[5] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonRight;
        Keypad_debugPrintf("Pressed button Right\n");
      }
      if ((s_kButtonsValues[4] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[4] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonLargeSolenoidOnOff;
        Keypad_debugPrintf("Pressed button Large Solenoid On/Off\n");
      }
      if ((s_kButtonsValues[11] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[11] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonStartFaceoff;
        Keypad_debugPrintf("Pressed button Start Faceoff\n");
      }
      if ((s_kButtonsValues[9] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[9] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonDown;
        Keypad_debugPrintf("Pressed button Down\n");
      }
      if ((s_kButtonsValues[6] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[6] < (l_val + s_kButtonValueDeadZone))){
      //if (l_val == s_kButtonsValues[6]) {
        pressedButton = k_buttonSmallSolenoidOnOff;
        Keypad_debugPrintf("Pressed button Small Solenoid On/Off\n");
      }
      if ((s_kButtonsValues[2] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[2] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonMotorRotateCCW;
        Keypad_debugPrintf("Pressed button Motor Rotate CCW\n");
      }
      if ((s_kButtonsValues[3] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[3] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonKillAll;
        Keypad_debugPrintf("Pressed button Kill All\n");
      }
      if ((s_kButtonsValues[1] > (l_val - s_kButtonValueDeadZone)) && (s_kButtonsValues[1] < (l_val + s_kButtonValueDeadZone))){
        pressedButton = k_buttonMotorRotateCW;
        Keypad_debugPrintf("Pressed button Motor Rotate CW\n");
      }
      
      if (l_val != 0) {
        s_isPresed = true;
        s_keypadState = k_KeypadReleaseWait;
      }
      break;
    case k_KeypadReleaseWait:
      if (l_val == 0) {
        s_keypadState = k_KeypadBounceWait;
        s_buttonBounceTime = millis();
      }
      break;
    case k_KeypadBounceWait:
      if (millis() - s_buttonBounceTime > l_kButtonBounseDelay) {
        s_keypadState = k_KeypadWait;
      }
      break;
  }
}

bool Keypad_isPressed()
{
  if(s_isPresed){
    s_isPresed = false;
    return true;
  }
  else
    return false;
}

Button_t Keypad_getPressedButton()
{
  return pressedButton; 
}

