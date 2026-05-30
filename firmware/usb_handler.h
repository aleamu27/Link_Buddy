#ifndef USB_HANDLER_H
#define USB_HANDLER_H

#include <Arduino.h>
#include "states.h"

extern QueueHandle_t stateQueue;

void TaskUsbListener(void *pvParameters) {
  LinkBuddyState currentState = STATE_ONBOARDING;
  unsigned long lastPingTime = millis();
  bool appConnected = false;

  for (;;) {
    if (Serial.available() > 0) {
      String input = Serial.readStringUntil('\n');
      input.trim();

      if (input == "PING_FROM_PC_APP") {
        appConnected = true;
        lastPingTime = millis();
        currentState = STATE_NORMAL;
        xQueueSend(stateQueue, &currentState, portMAX_DELAY);
      }
      else if (input == "CMD_ANALYZING") {
        currentState = STATE_ANALYZING;
        xQueueSend(stateQueue, &currentState, portMAX_DELAY);
      }
      else if (input == "CMD_SAFE") {
        currentState = STATE_SAFE;
        xQueueSend(stateQueue, &currentState, portMAX_DELAY);
      }
      else if (input == "CMD_UNSAFE") {
        currentState = STATE_UNSAFE;
        xQueueSend(stateQueue, &currentState, portMAX_DELAY);
      }
    }

    if (appConnected && (millis() - lastPingTime > 5000)) {
      appConnected = false;
      currentState = STATE_ONBOARDING;
      xQueueSend(stateQueue, &currentState, portMAX_DELAY);
    }

    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

#endif
