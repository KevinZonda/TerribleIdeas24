from flask import Flask, request, jsonify
from transformers import pipeline
import numpy as np
import base64
import io
from pydub import AudioSegment
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

# Initialize the ASR pipeline
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-small", device=0)
# Initialize the TTS pipeline
synthesiser = pipeline("text-to-speech", model="microsoft/speecht5_tts", device=0)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

@app.route('/asr', methods=['POST'])
def asr():
    # Parse the received audio data
    data: dict = request.get_json()
    # TODO: use json schema or something to validate the data
    encoded_audio = data['bytes']  # required
    
    # Decode the Base64 audio bytes
    audio_bytes = base64.b64decode(encoded_audio)
    
    # Convert audio bytes to an AudioSegment object using pydub
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))  # automatic decides format
    
    # Convert AudioSegment to raw audio data (numpy array)
    audio_array = np.array(audio.get_array_of_samples())
    
    # Ensure the audio is mono (1 channel)
    if audio.channels > 1:
        audio = audio.set_channels(1)
    
    # Process the audio with the ASR pipeline
    transcript = transcriber(
        {
            "sampling_rate": audio.frame_rate,
            "raw": audio_array.astype(np.float32) / np.max(np.abs(audio_array)),
        }
    )
    return jsonify({
        "text": transcript["text"]
    })

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
    
    return jsonify({"audio": encoded_audio, "sampling_rate": speech["sampling_rate"]})


if __name__ == '__main__':
     app.run(host='127.0.0.1', port=11451)
