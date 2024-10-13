#include <ESP32Servo.h>
#include "btn.h"

#define PIN_LED 12
#define PIN_BTN_IN 15
#define PIN_SG90 13

#define SERVO_DELAY_TIME 500

btn * btn_in;

Servo sg90;

bool is_on = false;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_LED, OUTPUT);
  btn_in = btn_init(PIN_BTN_IN);
  sg90.setPeriodHertz(50);
  sg90.attach(PIN_SG90);
}


unsigned long _curtime = 0;
unsigned long _servo_time = 0;
unsigned long delay_start = 0;
int _servo_next_action = 90;

int servo_action_iter() {
  int act = _servo_next_action;
  _servo_next_action = - _servo_next_action;
  return act;
}


void servo_next_state() {
  sg90.write(servo_action_iter());
  _servo_time = millis();
}


void btn_servo_sync() {
  bool is_changed = btn_scan(btn_in);
  if (!is_changed) {
      if (_servo_time - _curtime >= SERVO_DELAY_TIME && is_on) {
        servo_next_state();
    }
    return;
  }


  if (btn_scan(btn_in)) {
    is_on = !is_on;
    if (is_on) {
      servo_next_state();
    } else {
      sg90.write(0);
    }
    
  }
}

void loop() {
  _curtime = millis();
  btn_servo_sync();
  Serial.println(is_on ? "btn_scan_T" : "btn_scan_F");
}
