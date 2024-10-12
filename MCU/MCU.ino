#include <Arduino.h>
#include <ESP32Servo.h>


#define PIN_SG90 13 // Output pin used
Servo sg90;
#include <ESP32Servo.h>


#define PIN_SG90 13 // Output pin used
Servo sg90;

void setup() {
  sg90.setPeriodHertz(50); // PWM frequency for SG90
  sg90.attach(PIN_SG90); // Minimum and maximum pulse width (in µs) to go from 0° to 180
}

void loop() {
  sg90.write(90);
  delay(500);
  sg90.write(-90);
  delay(500);
}
