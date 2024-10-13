
#ifndef TERRIBLE_BTN_H
#define TERRIBLE_BTN_H

#include "Arduino.h"

typedef struct _btn {
    int pin;
    int state;
} btn;


btn * btn_init(int pin) {
    btn * ptr = (btn *) malloc(sizeof(pin));
    ptr->pin = pin;
    pinMode(pin, INPUT);
    return ptr;
}


bool btn_scan(btn * b) {
    int current_state = digitalRead(b->pin);
    bool state_changed = b->state != current_state;
    b->state = current_state;
    return state_changed && b->state == LOW;
}

#endif