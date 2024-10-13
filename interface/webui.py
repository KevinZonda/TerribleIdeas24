import streamlit as st
from streamlit_mic_recorder import mic_recorder
import base64
import requests

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from api.llm import gpt_response

st.set_page_config(
    page_title="Terrible Ideas - I's Shaking",
    page_icon="👀",
    layout="centered",
    initial_sidebar_state="expanded",
)

'''
This is to be run locally on your machine so that the browser lets you access the microphone through http
'''

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "audio" not in st.session_state:
    st.session_state.audio = None

# def send_audio(audio_bytes, reply_method, prompt_suffix, send_to_stream, url="http://0.0.0.0:7861/asr"):
def send_audio_for_asr(audio_bytes, url="http://127.0.0.1:11451/asr"):
    audio_bytes = base64.b64encode(audio_bytes).decode('utf-8')
    audio_data = {"bytes": audio_bytes}
    response = requests.post(url, json=audio_data)
    if response.status_code == 200:
        print("Audio sent successful!")
        return response.json()
    else:
        print(f"Failed to send audio. Status code: {response.status_code}")

def send_text_for_tts(text, url="http://127.0.0.1:11451/tts"):
    data = {"text": text}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Text sent successful!")
        return response.json()
    else:
        print(f"Failed to send text. Status code: {response.status_code}")

def decode_audio_from_tts(audio_bytes):
    return base64.b64decode(audio_bytes)

def send_audio_to_bot(audio_bytes, url="http://0.0.0.0:11451/receive_audio"):  # TODO: change the URL
    audio_bytes = base64.b64encode(audio_bytes).decode('utf-8')
    audio_data = {"audio": audio_bytes}
    response = requests.post(url, json=audio_data)
    if response.status_code == 200:
        print("Audio sent successful!")
        return response.json()
    else:
        print(f"Failed to send audio. Status code: {response.status_code}")

with st.container():
    st.write("Audio Recorder:")
    audio = mic_recorder(
        start_prompt="start the recording",
        stop_prompt="stop the recording",
        just_once=False,
        use_container_width=True,
        callback=None,
        args=(),
        kwargs={},
        key=None,
    )
    if audio is not None:
        st.session_state.audio = audio["bytes"]
    uploaded_audio = st.file_uploader("Upload Audio File", type=["wav", "mp3"])
    if uploaded_audio is not None:
        st.session_state.audio = uploaded_audio.read()
    if st.session_state.audio is not None:
        st.audio(st.session_state.audio, format="audio/wav")
        if st.button("Send Audio"):
            asr_resp = send_audio_for_asr(st.session_state.audio)
            st.session_state["chat_history"].append(
                {"role": "user", "content": asr_resp["text"]}
            )

            # LLM reply
            prompt, gpt_resp = gpt_response(asr_resp["text"])

            tts_resp = send_text_for_tts(gpt_resp)

            audio = decode_audio_from_tts(tts_resp["audio"])
            st.audio(audio, format="audio/wav")
            # bot_resp = send_audio_to_bot(audio)

            st.session_state["chat_history"].append(
                {"role": "assistant", "content": gpt_resp}
            )
            

for ith_history in st.session_state["chat_history"]:
    with st.chat_message(name=ith_history["role"]):
        st.write(ith_history["content"])
