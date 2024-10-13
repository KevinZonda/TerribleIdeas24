from flask import Flask, request, jsonify
from transformers import pipeline
import numpy as np
import base64
import requests
import wave
import io
from pydub import AudioSegment
import scipy
from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch

app = Flask(__name__)

# Initialize the TTS pipeline
synthesiser = pipeline("text-to-speech", model="microsoft/speecht5_tts", device=0)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

@app.route('/tts', methods=['POST'])
def tts():
    # Parse the received audio data
    data: dict = request.get_json()
    text = data['text']  # required
    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})
    
    # Convert the audio to a byte stream
    byte_io = io.BytesIO()
    scipy.io.wavfile.write(byte_io, rate=speech["sampling_rate"], data=speech["audio"])
    byte_io.seek(0)
    
    # Encode the byte stream to base64
    encoded_audio = base64.b64encode(byte_io.read()).decode('utf-8')
    
    return jsonify({"audio": encoded_audio})


if __name__ == '__main__':
     app.run(host='127.0.0.1', port=7862)
