#include "btn.h"

#define PIN_LED 12
#define PIN_BTN_IN 22

btn * btn_in;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  btn_in = btn_init(PIN_BTN_IN);

}

bool is_on = false;

void loop() {
  digitalWrite(PIN_LED, HIGH);
  sleep(1000);
  digitalWrite(PIN_LED, LOW);
  sleep(1000);

  if (btn_scan(btn_in)) {
    is_on = !is_on;
  }
}
