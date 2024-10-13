import streamlit as st
import base64
import requests
import time

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


def send_text_for_tts(text, url="http://127.0.0.1:11451/tts"):
    data = {"text": text}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Text sent successful!")
        return response.json()
    else:
        print(f"Failed to send text. Status code: {response.status_code}")

def get_text_and_play_audio():
    prompt, gpt_resp = gpt_response()
    response = send_text_for_tts(gpt_resp)
    audio_bytes = base64.b64decode(response["audio"])
    st.audio(audio_bytes, format="audio/wav", autoplay=True)
    return gpt_resp, len(audio_bytes) / (response['sampling_rate'] * 4)

def update_chat_history(gpt_resp):
    container = st.session_state["chat_container"]
    container.write(gpt_resp)

message_container = st.chat_message(name="assistant")
st.session_state["chat_container"] = message_container

while True:
    gpt_resp, audio_length = get_text_and_play_audio()
    update_chat_history(gpt_resp)
    time.sleep(audio_length)
