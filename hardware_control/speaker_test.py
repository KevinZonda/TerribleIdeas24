import serial
import wave
import time

# Configure the serial port

ser = serial.Serial('COM5', 115200)  # Replace with your ESP32's port


with open('./hardware_control/speech.wav', 'rb') as wav_file:
    chunk_size = 1  # Number of bytes to send at a time
    sample_rate = 8000
    delay = 1 / sample_rate  # Delay between chunks
    # Read audio data and send it to ESP32
    while True:
        chunk = wav_file.read(chunk_size)
        if not chunk:
            break  # End of file

        # Send the byte to the ESP32 over USB serial
        ser.write(chunk)

        # Add a small delay to prevent flooding the serial buffer
        time.sleep(delay)

    # Close the serial connection
    ser.close()
