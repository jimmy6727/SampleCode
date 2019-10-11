#ifndef MENU_H
#define MENU_H

#include "Keypad.h"
#include <stdint.h>
#include <vector>

#define MENU_DEBUG  

#define MENU_NAME_SIZE (20)
#define ITEM_NAME_SIZE (20)

#ifdef __cplusplus
extern "C" {
#endif

typedef struct ArrayFloatValueItem{
  void *ptr;
  uint8_t index;
  uint8_t size;
}ArrayValueItem_t;

typedef struct IntValueItem{
  int32_t value;
  int32_t delta;
  int32_t minLimit;
  int32_t maxLimit;
  ArrayValueItem_t arr;
}IntValueItem_t;

typedef struct FloatValueItem{
  float value;
  float delta;
  float minLimit;
  float maxLimit;
  ArrayValueItem_t arr;
}FloatValueItem_t;

typedef enum itemId {
  REACTION_TIME_ITEM,
  SPRING_FORCE_ITEM,
  PLAY_ITEM,
  RELEASE_ITEM,
  RETURN_ITEM,
  LOADED_ITEM,
  SET_POSITION_ITEM
} itemId;

typedef enum typeValue {
  NO_VALUE,
  INT_VALUE,
  FLOAT_VALUE
} TypeValue_t;

typedef struct Item{
  uint8_t id;
  char name[ITEM_NAME_SIZE];
  uint8_t typeValue;
  union{
      IntValueItem_t intValue;
      FloatValueItem_t floatValue;
  };
}Item_t;

typedef enum menuEvent{NONE_MENU_STATE, INPUT_MENU_STATE} MenuEvent_t;

typedef struct Menu{
  char name[MENU_NAME_SIZE];
  uint8_t selectedItem;
  bool isImputState;
  std::vector <Item_t> vItems;
}Menu_t;

void Menu_init();
void Menu_control(Button_t pressedButton);
void Menu_add(Menu_t *menu, char* name);
void Menu_addItem(Menu_t *menu, uint8_t id, char *name);
bool Menu_addIntValueItem(Item_t *item, int32_t value, int32_t delta, int32_t minLimit, int32_t maxLimit);
bool Menu_addFloatValueItem(Item_t *item, float value, float delta, float minLimit, float maxLimit);
bool Menu_addArrayIntValueItem(Item_t *item, float *pArray, uint8_t currentIndex, uint8_t sizeArray);
bool Menu_addArrayFloatValueItem(Item_t *item, float *pArray, uint8_t currentIndex, uint8_t sizeArray);
void Menu_callback(Item_t *item);
void Menu_process();
void Menu_manualHandler(Button_t pressedButton);

#ifdef __cplusplus
}
#endif

#endif // MENU_H

