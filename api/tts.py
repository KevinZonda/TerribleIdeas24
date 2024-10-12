from flask import Flask, request, jsonify
from transformers import pipeline
import numpy as np
import base64
import requests
import wave
import io
from pydub import AudioSegment
import scipy

app = Flask(__name__)

# Initialize the ASR pipeline
synthesiser = pipeline("text-to-speech", model="suno/bark-small", device=0)
# currently not configured to use gpu
@app.route('/tts', methods=['POST'])
def tts():
    # Parse the received audio data
    data: dict = request.get_json()
    text = data['text']  # required
    speech = synthesiser(text, forward_params={"do_sample": True})
    
    # Convert the audio to a byte stream
    byte_io = io.BytesIO()
    scipy.io.wavfile.write(byte_io, rate=speech["sampling_rate"], data=speech["audio"])
    byte_io.seek(0)
    
    # Encode the byte stream to base64
    encoded_audio = base64.b64encode(byte_io.read()).decode('utf-8')
    
    return jsonify({"audio": encoded_audio})


if __name__ == '__main__':
     app.run(host='127.0.0.1', port=7862)
