#include <WiFi.h>
#include "Terrible.h"

void init_wifi_module() {
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
}

void scan_wifi() {
    Serial.println("scan start");
    int n = WiFi.scanNetworks();
    Serial.println("scan done");
    if (n == 0) {
        Serial.println("no networks found");
        return;
    }

    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
        // Print SSID and RSSI for each network found
        Serial.print(i + 1);
        Serial.print(": ");
        Serial.print(WiFi.SSID(i));
        Serial.print(" (");
        Serial.print(WiFi.RSSI(i));
        Serial.print(")");
        Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
        delay(10);
    }
}

connection_counter * init_connection_counter() {
    connection_counter *ptr = malloc(sizeof(connection_counter));
    ptr->ctr = 0;
    return ptr;
}

const char* ssid = "REPLACE_WITH_YOUR_SSID";
const char* password = "REPLACE_WITH_YOUR_PASSWORD";
void connwct_wifi(connection_counter * ctr) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi ..");
    while (WiFi.status() != WL_CONNECTED && connection_counter->ctr <= 5) {
        Serial.print('.');
        delay(1000);
    }

    Serial.println(WiFi.status() == WL_CONNECTED ? WiFi.localIP() : FAILURE);
}