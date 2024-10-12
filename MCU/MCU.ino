#define PIN_LED D12

void setup() {
  pinMode(PIN_LED, OUTPUT);

}

void loop() {
  digitalWrite(PIN_LED, HIGH);
  sleep(1000);
  digitalWrite(PIN_LED, LOW);
  sleep(1000);
}
