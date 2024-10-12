from flask import Flask, request, jsonify
from transformers import pipeline
import numpy as np
import base64
import io
from pydub import AudioSegment

app = Flask(__name__)

# Initialize the ASR pipeline
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-small", device=0)
# currently not configured to use gpu
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


if __name__ == '__main__':
     app.run(host='127.0.0.1', port=7861)
