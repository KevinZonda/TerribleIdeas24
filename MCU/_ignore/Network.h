#ifndef STUDENT_H
#define STUDENT_H

typedef struct _network_connection_counter {
    int ctr;
} connection_counter;


connection_counter * init_connection_counter();
void connwct_wifi(connection_counter * ctr);
void init_wifi_module();
void scan_wifi();

#endif