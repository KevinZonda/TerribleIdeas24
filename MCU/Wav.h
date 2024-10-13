#include <driver/dac.h>

const int dacPin = 14;  // DAC1, GPIO25 (you can also use GPIO26 for DAC2)
const int bufferSize = 1024;
uint8_t audioBuffer[bufferSize];

void init_dac() {
  Serial.begin(115200);
  dac_output_enable(DAC_CHANNEL_1);  // Enable DAC on GPIO25
}

void play_audio() {
  if (Serial.available() >= bufferSize) {
    // Read audio data from serial
    Serial.readBytes(audioBuffer, bufferSize);
    
    // Output audio data to DAC
    for (int i = 0; i < bufferSize; i++) {
      dac_output_voltage(DAC_CHANNEL_1, audioBuffer[i]);
      delayMicroseconds(125);  // Adjust this delay based on your sample rate
    }
  }
}