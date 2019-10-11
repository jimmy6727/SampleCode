#include "Motor.h"

#ifdef  MOTOR_DEBUG  
#define Lcd_debugPrintf(...) Serial.printf(__VA_ARGS__);
#else 
#define Lcd_debugPrintf(...);
#endif

static const uint8_t k_SolenoidReleaseVoltage = 255;
static const uint8_t k_SolenoidReturnVoltage = 255;

void Motor_init()
{
  ledcSetup(k_MotorDirectionCW, 4000, 8);
  ledcSetup(k_MotorDirectionCCW, 4000, 8);
  ledcAttachPin(MOTOR_FORWARD_PIN, k_MotorDirectionCW);
  ledcAttachPin(MOTOR_REVERSE_PIN, k_MotorDirectionCCW);
  pinMode(MOTOR_FORWARD_PIN, OUTPUT);
  pinMode(MOTOR_REVERSE_PIN, OUTPUT);
  pinMode(LIMIT_SWITCH_PIN, INPUT);
  Motor_stop();
}

void Motor_rotate(MotorDirection_t direction, uint8_t speed)
{
  switch(direction){
    case k_MotorDirectionCW:
      ledcWrite(k_MotorDirectionCW, 0);
      ledcWrite(k_MotorDirectionCCW, 0);
      break;
    case k_MotorDirectionCCW:
      ledcWrite(k_MotorDirectionCW, 0);
      ledcWrite(k_MotorDirectionCCW, 255);
      break;
  }
}

void Motor_stop()
{
  ledcWrite(k_MotorDirectionCW, 255);
  ledcWrite(k_MotorDirectionCCW, 0);
}

bool Motor_isLimitSwitch()
{
  if(digitalRead(LIMIT_SWITCH_PIN))
    return true;
  else
    return false;
}

void Solenoid_init()
{
  ledcSetup(k_SolenoidRelease, 4000, 8);
  ledcSetup(k_SolenoidReturn, 4000, 8);
  ledcAttachPin(SOLENOID_RELEASE_PIN, k_SolenoidRelease);
  ledcAttachPin(SOLENOID_RETURN_PIN, k_SolenoidReturn);
  pinMode(SOLENOID_RELEASE_PIN, OUTPUT);
  pinMode(SOLENOID_RETURN_PIN, OUTPUT);
}

void Solenoid_switch(Solenoid_t soleniod, SolenoidState_t state)
{
  if(state == k_SolenoidOn){
    switch(soleniod){
      case k_SolenoidRelease:
        ledcWrite(soleniod, k_SolenoidReleaseVoltage); 
        break;
      case k_SolenoidReturn:
        ledcWrite(soleniod, k_SolenoidReturnVoltage); 
        break;
    }
  }
  else{
    ledcWrite(soleniod, 0);
  }
}

