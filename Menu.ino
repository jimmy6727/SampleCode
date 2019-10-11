#include "Menu.h"
#include "ArmControl.h"
#include "LCD.h"

#ifdef  MENU_DEBUG
#define Menu_debugPrintf(...) Serial.printf(__VA_ARGS__);
#else
#define Menu_debugPrintf(...);
#endif

static Menu_t s_mainMenu;
static Menu_t *s_pCurrentMenu;

static float s_arrSpringForce[3] = {3.5, 7.0, 10.0};

void Menu_init()
{
  Menu_add(&s_mainMenu, "Main menu");
  /*Menu_addItem(&s_mainMenu, SPRING_FORCE_ITEM, "Spring force(ld)");
    Menu_addArrayFloatValueItem(&s_mainMenu.vItems[SPRING_FORCE_ITEM], s_arrSpringForce, 0, 3);*/
  Menu_addItem(&s_mainMenu, REACTION_TIME_ITEM, "Reaction time(ms)");
  Menu_addIntValueItem(&s_mainMenu.vItems[REACTION_TIME_ITEM], 200, 10, 0, 400);
  Menu_addItem(&s_mainMenu, SPRING_FORCE_ITEM, "Set position");
  Menu_addIntValueItem(&s_mainMenu.vItems[SPRING_FORCE_ITEM], 0, 1, 0, 2);

  Menu_addItem(&s_mainMenu, RELEASE_ITEM, "Release");
  Menu_addItem(&s_mainMenu, RETURN_ITEM, "Return");
  s_pCurrentMenu = &s_mainMenu;
  Menu_control(k_buttonNone);
}

void Menu_add(Menu_t *menu, char* name)
{
  memcpy(menu->name, name, MENU_NAME_SIZE);
  menu->selectedItem = 0;
}

void Menu_addItem(Menu_t *menu, uint8_t id, char *name)
{
  Item_t entryItem;
  entryItem.id = id;
  memcpy(entryItem.name, name, ITEM_NAME_SIZE);
  entryItem.typeValue = NO_VALUE;
  menu->vItems.push_back(entryItem);
}

bool Menu_addIntValueItem(Item_t *item, int32_t value, int32_t delta, int32_t minLimit, int32_t maxLimit)
{
  if (delta < 0)
    return false;
  if ((value > maxLimit) || (value < minLimit))
    return false;
  item->intValue.arr.ptr = NULL;
  item->intValue.value = value;
  item->intValue.delta = delta;
  item->intValue.maxLimit = maxLimit;
  item->intValue.minLimit = minLimit;
  item->typeValue = INT_VALUE;
  return true;
}

bool Menu_addFloatValueItem(Item_t *item, float value, float delta, float minLimit, float maxLimit)
{
  if (delta < 0)
    return false;
  if ((value > maxLimit) || (value < minLimit))
    return false;
  item->floatValue.arr.ptr = NULL;
  item->floatValue.value = value;
  item->floatValue.delta = delta;
  item->floatValue.maxLimit = maxLimit;
  item->floatValue.minLimit = minLimit;
  item->typeValue = FLOAT_VALUE;
  return true;
}

bool Menu_addArrayIntValueItem(Item_t *item, int32_t *pArray, uint8_t currentIndex, uint8_t sizeArray)
{
  if (pArray == NULL)
    return false;
  if ((currentIndex >= sizeArray) || (currentIndex < 0))
    return false;
  item->intValue.arr.ptr = pArray;
  item->intValue.arr.index = currentIndex;
  item->intValue.arr.size = sizeArray;
  item->intValue.value = *((int*)item->intValue.arr.ptr + item->intValue.arr.index);
  item->typeValue = INT_VALUE;
  return true;
}

bool Menu_addArrayFloatValueItem(Item_t *item, float *pArray, uint8_t currentIndex, uint8_t sizeArray)
{
  if (pArray == NULL)
    return false;
  if ((currentIndex >= sizeArray) || (currentIndex < 0))
    return false;
  item->floatValue.arr.ptr = pArray;
  item->floatValue.arr.index = currentIndex;
  item->floatValue.arr.size = sizeArray;
  item->floatValue.value = *((float*)item->floatValue.arr.ptr + item->floatValue.arr.index);
  item->typeValue = FLOAT_VALUE;
  return true;
}

bool Menu_incDecFloat(FloatValueItem_t *value, bool inc)
{
  if (inc) {
    if (value->arr.ptr != NULL) {
      if (value->arr.index + 1 < value->arr.size) {
        value->arr.index++;
        value->value = *((float*)value->arr.ptr + value->arr.index);
      }
      else
        return false;
    }
    else {
      if ((value->value + value->delta) > value->maxLimit)
        return false;
      value->value += value->delta;
    }
  }
  else {
    if (value->arr.ptr != NULL) {
      if (value->arr.index - 1 >= 0) {
        value->arr.index--;
        value->value = *((float*)value->arr.ptr + value->arr.index);
      }
      else
        return false;
    }
    if ((value->value - value->delta) < value->minLimit)
      return false;
    value->value -= value->delta;
  }
  Menu_debugPrintf("value->value %f\n", value->value);
  return true;
}

bool Menu_incDecInt(IntValueItem_t *value, bool inc)
{
  if (inc) {
    if (value->arr.ptr != NULL) {
      if (value->arr.index + 1 < value->arr.size) {
        value->arr.index++;
        value->value = *((int*)value->arr.ptr + value->arr.index);
      }
      else
        return false;
    }
    else {
      if ((value->value + value->delta) > value->maxLimit)
        return false;
      value->value += value->delta;
    }
  }
  else {
    if (value->arr.ptr != NULL) {
      if (value->arr.index - 1 >= 0) {
        value->arr.index--;
        value->value = *((int*)value->arr.ptr + value->arr.index);
      }
      else
        return false;
    }
    if ((value->value - value->delta) < value->minLimit)
      return false;
    value->value -= value->delta;
  }
  return true;
}

void Menu_manualHandler(Button_t pressedButton)
{
  static bool l_stateLargeSolenoid = false;
  static bool l_stateSmallSolenoid = false;
  static bool l_isMotorRotate = false;

  /*if (pressedButton == k_buttonMotorRotateCW){
    Motor_rotate(k_MotorDirectionCW, k_MotorMaxSpeed);
    return;
    }*/

  if (pressedButton == k_buttonMotorRotateCW) {
    if (l_isMotorRotate) {
      Motor_stop();
      l_isMotorRotate = false;
    }
    else {
      Motor_rotate(k_MotorDirectionCW, k_MotorMaxSpeed);
      l_isMotorRotate = true;
    }
    return;
  }

  if (pressedButton == k_buttonMotorRotateCCW) {
    if (l_isMotorRotate) {
      Motor_stop();
      l_isMotorRotate = false;
    }
    else {
      Motor_rotate(k_MotorDirectionCCW, k_MotorMaxSpeed);
      l_isMotorRotate = true;
    }
    return;
  }

  /*if (pressedButton == k_buttonMotorRotateCCW){
    Motor_rotate(k_MotorDirectionCCW, k_MotorMaxSpeed);
    return;
    }*/
  if (pressedButton == k_buttonKillAll) {
    Motor_stop();
    l_isMotorRotate = false;
    Solenoid_switch(k_SolenoidRelease, k_SolenoidOff);
    l_stateLargeSolenoid = false;
    Solenoid_switch(k_SolenoidReturn, k_SolenoidOff);
    l_stateSmallSolenoid = false;
    return;
  }
  if (pressedButton == k_buttonLargeSolenoidOnOff) {
    if (l_stateLargeSolenoid) {
      Solenoid_switch(k_SolenoidRelease, k_SolenoidOff);
      l_stateLargeSolenoid = false;
    }
    else {
      Solenoid_switch(k_SolenoidRelease, k_SolenoidOn);
      l_stateLargeSolenoid = true;
    }
    return;
  }
  if (pressedButton == k_buttonSmallSolenoidOnOff) {
    if (l_stateSmallSolenoid) {
      Solenoid_switch(k_SolenoidReturn, k_SolenoidOff);
      l_stateSmallSolenoid = false;
    }
    else {
      Solenoid_switch(k_SolenoidReturn, k_SolenoidOn);
      l_stateSmallSolenoid = true;
    }
    return;
  }
  if (pressedButton == k_buttonStartFaceoff) {
    Motor_stop();
    l_isMotorRotate = false;
    Solenoid_switch(k_SolenoidRelease, k_SolenoidOff);
    l_stateLargeSolenoid = false;
    Solenoid_switch(k_SolenoidReturn, k_SolenoidOff);
    l_stateSmallSolenoid = false;
    Arm_faceoff();
    return;
  }
}

void Menu_control(Button_t pressedButton)
{
  static float s_floatBackUp = 0;
  static uint32_t s_intBackUp = 0;
  static uint8_t s_indexBackUp = 0;
  static MenuEvent_t l_menuState = NONE_MENU_STATE;

  switch (l_menuState) {
    case NONE_MENU_STATE:
      if (pressedButton == k_buttonSet) {
        if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue != NO_VALUE) {
          l_menuState = INPUT_MENU_STATE;
          if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue == INT_VALUE) {
            s_intBackUp = s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue.value;
            if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue.arr.ptr != NULL)
              s_indexBackUp = s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue.arr.index;
          }
          if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue == FLOAT_VALUE) {
            s_floatBackUp = s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].floatValue.value;
            if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].floatValue.arr.ptr != NULL)
              s_indexBackUp = s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue.arr.index;
          }
        }
        else {
          Menu_callback(&s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem]);
        }
      }
      break;
    case INPUT_MENU_STATE:
      if ((pressedButton == k_buttonUp) || (pressedButton == k_buttonDown)) {
        l_menuState = NONE_MENU_STATE;
        if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue == INT_VALUE) {
          s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue.value = s_intBackUp;
          if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue.arr.ptr != NULL)
            s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue.arr.index = s_indexBackUp;
        }
        if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue == FLOAT_VALUE) {
          s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].floatValue.value = s_floatBackUp;
          if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].floatValue.arr.ptr != NULL)
            s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].floatValue.arr.index = s_indexBackUp;
        }
      }
      if (pressedButton == k_buttonSet) {
        l_menuState = NONE_MENU_STATE;
        Menu_callback(&s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem]);

      }
      if (pressedButton == k_buttonLeft) {
        if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue == INT_VALUE) {
          Menu_incDecInt(&s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue, false);
        }
        if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue == FLOAT_VALUE) {
          Menu_incDecFloat(&s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].floatValue, false);
        }

      }
      if (pressedButton == k_buttonRight) {
        if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue == INT_VALUE) {
          Menu_incDecInt(&s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].intValue, true);
        }
        if (s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].typeValue == FLOAT_VALUE) {
          Menu_incDecFloat(&s_pCurrentMenu->vItems[s_pCurrentMenu->selectedItem].floatValue, true);
        }
      }
      break;
  }

  if (pressedButton == k_buttonUp) {
    if (s_pCurrentMenu->selectedItem != 0)
      s_pCurrentMenu->selectedItem--;
  }
  if (pressedButton == k_buttonDown) {
    if (s_pCurrentMenu->selectedItem != s_pCurrentMenu->vItems.size() - 1)
      s_pCurrentMenu->selectedItem++;
  }

  LCD_displayMenu(s_pCurrentMenu, l_menuState);

}

void Menu_process()
{
  if (Keypad_isPressed()) {
    Button_t l_pressedButton = Keypad_getPressedButton();
    Menu_debugPrintf("pressedButton %d\n", l_pressedButton);
    Menu_control(l_pressedButton);
    Menu_manualHandler(l_pressedButton);
  }
}

void Menu_callback(Item_t *item)
{
  switch (item->id) {
    case REACTION_TIME_ITEM:
      Arm_setRectionTime(item->intValue.value);
      break;
    case PLAY_ITEM:
      static uint8_t numVoice = 0;
      mp3.asyncPlayVoice(numVoice);
      if (++numVoice > 3)
        numVoice = 0;
      break;
    case RELEASE_ITEM:
      Arm_release();
      break;
    case RETURN_ITEM:
      Arm_return();
      break;
    case SPRING_FORCE_ITEM:
      Menu_debugPrintf("Arm_setPosition, %d", item->intValue.value);
      if (item->intValue.value == 0) {
        Arm_setSpringForce(k_SpringForceMax);
        break;
      }
      if (item->intValue.value == 1) {
        Arm_setSpringForce(k_SpringForceMid);
        break;
      }
      if (item->intValue.value == 2) {
        Arm_setSpringForce(k_SpringForceMin);
        break;
      }
      break;
    default:
      break;
  }
}

