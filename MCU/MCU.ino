#include <Arduino.h>
#include <ESP32Servo.h>
#include "btn.h"

#define PIN_LED 12
#define PIN_BTN_IN 15
#define PIN_SG90 13
#define PIN_SPEAKER 14
#define SERVO_DETECT_SPLIT 200

btn * btn_in;

Servo sg90;

bool is_on = false;

void setup() {
  Serial.begin(9600);
  Serial2.begin(115200); //USB
  pinMode(PIN_SPEAKER, OUTPUT);
  pinMode(PIN_LED, OUTPUT);
  btn_in = btn_init(PIN_BTN_IN);
  sg90.setPeriodHertz(50); // PWM frequency for SG90
  sg90.attach(PIN_SG90); // Minimum and maximum pulse width (in µs) to go from 0° to 180
}


void _read_btn() {
  if (btn_scan(btn_in)) {
    is_on = !is_on;
  }
  if (!is_on) {
    sg90.write(0);
  }
}

// ret needExit
bool _delay_with_read_btn() {
  for (int i = 0; i < SERVO_DETECT_SPLIT; ++i) {
      _read_btn();
      if (!is_on) return true;
  }
  return false;
}

void play_audio() {
  if (Serial2.available() > 0) {
    byte incoming_byte = Serial2.read();
    // Output the audio byte as a digital signal
    for (int i = 0; i < 8; i++) {  // Iterate through each bit of the byte
      digitalWrite(PIN_SPEAKER, (incoming_byte & (1 << (7 - i))) ? HIGH : LOW);  // Set pin HIGH or LOW based on bit value
      delayMicroseconds(125);  // Adjust this delay based on your audio sample rate
    }
  }
}

void loop() {
  play_audio();

  _read_btn();
  Serial.println(is_on ? "btn_scanT" : "btn_scanF");

  if (is_on) {
    sg90.write(90);
    if (_delay_with_read_btn()) {
      return;
    }

    sg90.write(-90);
    if (_delay_with_read_btn()) {
      return;
    }
  }
}
