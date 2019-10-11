#ifndef MOTOR_H
#define MOTOR_H

#define MOTOR_DEBUG

#define MOTOR_FORWARD_PIN (12)
#define MOTOR_REVERSE_PIN (13)

#define SOLENOID_RELEASE_PIN (25)
#define SOLENOID_RETURN_PIN  (26)

#define LIMIT_SWITCH_PIN (35)

#ifdef __cplusplus
extern "C" {
#endif

const uint8_t k_MotorMaxSpeed = 255;

typedef enum MotorDirection{
  k_MotorDirectionCW = 3, 
  k_MotorDirectionCCW = 4
}MotorDirection_t;

typedef enum Solenoid{
  k_SolenoidRelease, 
  k_SolenoidReturn
}Solenoid_t;

typedef enum SolenoidState{
  k_SolenoidOff, 
  k_SolenoidOn
}SolenoidState_t;

void Motor_init();
void Motor_rotate(MotorDirection_t direction, uint8_t speed);
void Motor_stop();
bool Motor_isLimitSwitch();

void Solenoid_init();
void Solenoid_switch(Solenoid_t soleniod, SolenoidState_t state);

#ifdef __cplusplus
}
#endif

#endif
