#include <Arduino.h>
#include <ESP32Servo.h>
#include "btn.h"

#define PIN_LED 12
#define PIN_BTN_IN 15
#define PIN_SG90 13
#define Pin_SPEAKER 25

btn * btn_in;

Servo sg90;

bool is_on = false;

void setup() {
  Serial.begin(9600);
  Serial2.begin(115200); //USB

  pinMode(PIN_LED, OUTPUT);
  btn_in = btn_init(PIN_BTN_IN);
  sg90.setPeriodHertz(50); // PWM frequency for SG90
  sg90.attach(PIN_SG90); // Minimum and maximum pulse width (in µs) to go from 0° to 180
}

void loop() {
  if (Serial2.available()) {
    // Read the incoming byte from the USB serial
    byte audioByte = Serial.read();

    // Output the byte to the DAC pin (to speaker)
    dacWrite(Pin_SPEAKER, audioByte);
  }

  if (btn_scan(btn_in)) {
    is_on = !is_on;
  }
  Serial.println(is_on ? "btn_scanT" : "btn_scanF");

  if (is_on) {
    sg90.write(90);
    delay(500);
    sg90.write(-90);
    delay(500);
  }
}
