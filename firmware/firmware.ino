#include <Arduino.h>
#include "states.h"
#include "usb_handler.h"
#include "display_core.h"

QueueHandle_t stateQueue;

void setup() {
  Serial.begin(115200);

  // Opprett køen
  stateQueue = xQueueCreate(5, sizeof(LinkBuddyState));
  if (stateQueue == NULL) { while (1); }

  // Start USB-tråden på Kjerne 0
  xTaskCreatePinnedToCore(TaskUsbListener, "UsbListener", 4096, NULL, 2, NULL, 0);

  // Start Skjerm-tråden på Kjerne 1
  xTaskCreatePinnedToCore(TaskScreenRenderer, "ScreenRenderer", 4096, NULL, 1, NULL, 1);
}

void loop() {
  // FreeRTOS tar over, loopen slettes
  vTaskDelete(NULL);
}
