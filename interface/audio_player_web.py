import streamlit as st
from streamlit_mic_recorder import mic_recorder
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


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "audio" not in st.session_state:
    st.session_state.audio = None


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

    if "audio_start_time" not in st.session_state:
        st.session_state["audio_start_time"] = time.time()
    # Detect if the audio finishes playing
    audio_duration = len(audio_bytes) / (response['sampling_rate'] * 4)  # Assuming 16kHz sample rate and 16-bit audio
    st.write(f"Audio duration: {audio_duration:.2f} seconds")
    st.session_state["chat_history"].append(
                {"role": "assistant", "content": gpt_resp}
            )
    for ith_history in st.session_state["chat_history"]:
        with st.chat_message(name=ith_history["role"]):
            st.write(ith_history["content"])
    while time.time() - st.session_state["audio_start_time"] < audio_duration:
        time.sleep(1)
    st.session_state["audio_finished"] = True
    return True

    


# trigger the function continuously (and randomly?)
# st.session_state["audio_finished"] = True
# st.session_state["start"] = False

# if st.button("Start"):
#     st.session_state["start"] = True
# if st.button("Stop"):
#     st.session_state["start"] = False

while True:
    gpt_resp, audio_length = get_text_and_play_audio()
    st.session_state["chat_history"].append(
                {"role": "assistant", "content": gpt_resp}
            )
    for ith_history in st.session_state["chat_history"]:
        with st.chat_message(name=ith_history["role"]):
            st.write(ith_history["content"])
    time.sleep(audio_length)
