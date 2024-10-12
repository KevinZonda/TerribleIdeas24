
#ifndef TERRIBLE_BTN_H
#define TERRIBLE_BTN_H

#include "Arduino.h"

typedef struct _btn {
    int pin;
    int stat;
} btn;


btn * btn_init(int pin) {
    btn * ptr = (btn *) malloc(sizeof(pin));
    ptr->pin = pin;
    pinMode(pin, INPUT);
    return ptr;
}


bool btn_scan(btn * b) {
    int stat = digitalRead(b->pin);
    bool is_same = b->stat == stat;
    b->stat = stat;
    return is_same;
}

#endif