#include "ArmControl.h"
#include "WTV020SD16P.h"

WTV020SD16P mp3(CLOCK_MP3_PIN, DATA_MP3_PIN, BUSY_MP3_PIN);



static Arm_t s_armState;
static SpringForce_t s_springForce = k_SpringForceMax;
static uint32_t s_springLoadMaxTime;
static uint16_t s_reactionTime = 200;

void Arm_init()
{
  /*Motor_rotate(k_ArmDirectionDown, k_MotorMaxSpeed);
    delay(2000);
    Motor_stop();
    delay(500);
    Arm_release();
    Arm_return();
    Arm_release();*/


  /*s_springLoadMaxTime = (uint32_t)millis();
    Arm_return();
    s_springLoadMaxTime = (uint32_t)millis() - s_springLoadMaxTime;
    Arm_release();*/
}

void Arm_release()
{
  if (s_armState == k_armStateHomePosition) {
    delay(500);
    mp3.asyncPlayVoice(1);
    delay(2000);
    mp3.asyncPlayVoice(0);
    delay(2000);
    mp3.asyncPlayVoice(2);
    delay(300);
    delay(s_reactionTime);
    Solenoid_switch(k_SolenoidRelease, k_SolenoidOn);
    delay(1500);
    Solenoid_switch(k_SolenoidRelease, k_SolenoidOff);
    s_armState = k_armStateDownPosition;
  }
}

void Arm_faceoff()
{

  //if(s_armState == k_armStateDownPosition){
  Solenoid_switch(k_SolenoidRelease, k_SolenoidOn);
  Solenoid_switch(k_SolenoidReturn, k_SolenoidOn);
  Motor_rotate(k_ArmDirectionUp, k_MotorMaxSpeed);
  switch (s_springForce) {
    case k_SpringForceMax:
      while (!Motor_isLimitSwitch());
      break;
    case k_SpringForceMid:
      delay(4000);
      break;
    case k_SpringForceMin:
      delay(3000);
      break;
  }
  Motor_stop();
  Solenoid_switch(k_SolenoidRelease, k_SolenoidOff);
  Solenoid_switch(k_SolenoidReturn, k_SolenoidOff);
  Motor_rotate(k_ArmDirectionDown, k_MotorMaxSpeed);
  switch (s_springForce) {
    case k_SpringForceMax:
      delay(3800);
      break;
    case k_SpringForceMid:
      delay(2900);
      break;
    case k_SpringForceMin:
      delay(2400);
      break;
  }
  Motor_stop();
  s_armState = k_armStateHomePosition;
  //}
  //if(s_armState == k_armStateHomePosition){
  delay(500);
  mp3.asyncPlayVoice(1);
  delay(2000);
  mp3.asyncPlayVoice(0);
  delay(2000);
  mp3.asyncPlayVoice(2);
  delay(300);
  delay(s_reactionTime);
  Solenoid_switch(k_SolenoidRelease, k_SolenoidOn);
  delay(1500);
  Solenoid_switch(k_SolenoidRelease, k_SolenoidOff);
  s_armState = k_armStateDownPosition;
  //}
}

void Arm_setSpringForce(SpringForce_t springForce)
{
  if (springForce <= 2)
    s_springForce = springForce;
}

void Arm_return()
{
  if (s_armState == k_armStateDownPosition) {
    Solenoid_switch(k_SolenoidRelease, k_SolenoidOn);
    Solenoid_switch(k_SolenoidReturn, k_SolenoidOn);
    Motor_rotate(k_ArmDirectionUp, k_MotorMaxSpeed);
    switch (s_springForce) {
      case k_SpringForceMax:
        while (!Motor_isLimitSwitch());
        break;
      case k_SpringForceMid:
        delay(4000);
        break;
      case k_SpringForceMin:
        delay(3000);
        break;
    }
    Motor_stop();
    Solenoid_switch(k_SolenoidRelease, k_SolenoidOff);
    Solenoid_switch(k_SolenoidReturn, k_SolenoidOff);
    Motor_rotate(k_ArmDirectionDown, k_MotorMaxSpeed);
    switch (s_springForce) {
      case k_SpringForceMax:
        delay(3800);
        break;
      case k_SpringForceMid:
        delay(2900);
        break;
      case k_SpringForceMin:
        delay(2400);
        break;
    }
    Motor_stop();
    s_armState = k_armStateHomePosition;
  }
}

void Arm_setRectionTime(uint16_t reactTime)
{
  s_reactionTime = reactTime;
}
