#ifndef ARMCONTROL_H
#define ARMCONTROL_H

#ifdef __cplusplus
extern "C" {
#endif

typedef enum SpringForces{
  k_SpringForceMax,
  k_SpringForceMid,
  k_SpringForceMin
} SpringForce_t;

const MotorDirection_t k_ArmDirectionUp = k_MotorDirectionCCW;
const MotorDirection_t k_ArmDirectionDown = k_MotorDirectionCW;

typedef enum Arm {
  k_armStateHomePosition,
  k_armStateDownPosition,
  k_armStateRelease,
  k_armStateReturn
} Arm_t;

void Arm_init();
void Arm_faceoff();
void Arm_release();
void Arm_return();
void Arm_setSpringForce(SpringForce_t springForce);
void Arm_setRectionTime(uint16_t reactTime);

#ifdef __cplusplus
}
#endif

#endif
