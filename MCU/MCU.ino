#include <Arduino.h>
#include <ESP32Servo.h>
#include "btn.h"

#define PIN_LED 12
#define PIN_BTN_IN 22

btn * btn_in;

#define PIN_SG90 13 // Output pin used
Servo sg90;

bool is_on = false;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  btn_in = btn_init(PIN_BTN_IN);
  sg90.setPeriodHertz(50); // PWM frequency for SG90
  sg90.attach(PIN_SG90); // Minimum and maximum pulse width (in µs) to go from 0° to 180
}

void loop() {
  sg90.write(90);
  delay(500);
  sg90.write(-90);
  delay(500);
  digitalWrite(PIN_LED, HIGH);
  sleep(1000);
  digitalWrite(PIN_LED, LOW);
  sleep(1000);

  if (btn_scan(btn_in)) {
    is_on = !is_on;
  }
}
