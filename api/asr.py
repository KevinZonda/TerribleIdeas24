from flask import Flask, request, jsonify
from transformers import pipeline
import numpy as np
import base64
import requests
import wave
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
    # sample_rate = data['sample_rate']
    # reply_method = data.get('reply_method', "repeat")  # default to repeat
    # prompt_suffix = data.get('prompt_suffix', "")  # optional suffix for the prompt
    # send_to_stream = data.get('send_to_stream', False)  # optional flag to send to metahuman-stream
    
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

    # prepare the prompt
    # prompt = transcript["text"] + prompt_suffix

    # send to llm and return the response
    # if reply_method == "llm_qanything":
    #     llm = QAnything()
    # elif reply_method == "repeat":
    #     llm = Repeater()
    # else:
    #     return jsonify({"error": f"Invalid reply method -> {reply_method}"})
    # resp = llm.send_request(prompt)

    # send to metahuman-stream
    # if send_to_stream and resp is not None and resp != "None":
    #     submit_message(resp)

    # Return the result as JSON
    # return jsonify({"prompt": prompt, "response": resp})

if __name__ == '__main__':
     app.run(host='127.0.0.1', port=7861)





################################################################################################################################################

# import gradio as gr
# from transformers import pipeline
# import numpy as np

# transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")

# def transcribe(audio):
#     sr, y = audio
#     y = y.astype(np.float32)
#     y /= np.max(np.abs(y))

#     return transcriber({"sampling_rate": sr, "raw": y})["text"]  

# demo = gr.Interface(
#     transcribe,
#     gr.Audio(sources=["microphone"]),
#     "text",
# )

# demo.launch(server_name="0.0.0.0", server_port=7861)
