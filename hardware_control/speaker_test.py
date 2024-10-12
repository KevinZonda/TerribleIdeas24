import serial
import wave
import time

# Configure the serial port

ser = serial.Serial('COM5', 115200)  # Replace with your ESP32's port


with wave.open('./hardware_control/imperial.wav', 'rb') as wav_file:
    # Read audio data and send it to ESP32
    while True:
        audio_data = wav_file.readframes(1)  # Read one frame (one sample)
        if not audio_data:
            break  # Stop if we reach the end of the file

        # Send the byte to the ESP32 over USB serial
        ser.write(audio_data)

        # Add a small delay to prevent flooding the serial buffer
        time.sleep(0.001)  # 1 millisecond delay

    # Close the serial connection
    ser.close()
