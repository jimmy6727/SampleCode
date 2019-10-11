#ifndef KEYPAD_H
#define KEYPAD_H

#ifdef __cplusplus
extern "C" {
#endif

#define KEYPAD_DEBUG
#define KEYPAD_PIN (34)

typedef enum Button {
  k_buttonNone,
  k_buttonUp,
  k_buttonDown,
  k_buttonLeft,
  k_buttonRight,
  k_buttonSet,
  k_buttonMotorRotateCW,
  k_buttonMotorRotateCCW,
  k_buttonStartFaceoff,
  k_buttonLargeSolenoidOnOff,
  k_buttonSmallSolenoidOnOff,
  k_buttonKillAll
} Button_t;

void Keypad_init();
void Keypad_process();
bool Keypad_isPressed();
Button_t Keypad_getPressedButton();

#ifdef __cplusplus
}
#endif

#endif
