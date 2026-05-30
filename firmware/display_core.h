#ifndef DISPLAY_CORE_H
#define DISPLAY_CORE_H

#include <Arduino.h>
#include "states.h"

extern QueueHandle_t stateQueue;

// Her inkluderer du skjermbiblioteket ditt senere, f.eks:
// #include <Adafruit_SSD1306.h>

void TaskScreenRenderer(void *pvParameters) {
  LinkBuddyState drawState = STATE_ONBOARDING;
  
  // TODO: init_skjerm();

  for (;;) {
    // Sjekk om det har kommet en ny beskjed i postkassa
    if (xQueueReceive(stateQueue, &drawState, 0) == pdTRUE) {
      // Skjermen vet nå at den skal bytte fjes
    }

    // Tegn basert på humør
    switch (drawState) {
      case STATE_ONBOARDING:
        // Tegn QR og URL
        break;
      case STATE_NORMAL:
        // Tegn vanlig fjes
        break;
      case STATE_ANALYZING:
        // Tegn stressa fjes
        break;
      case STATE_SAFE:
        // Tegn smilefjes
        break;
      case STATE_UNSAFE:
        // Tegn kryss-øyne
        break;
    }

    vTaskDelay(pdMS_TO_TICKS(33)); // ~30 FPS
  }
}

#endif
