# Terrible Ideas 24
team I's Shaking (TBC)

## Task Breakdown
- Hardware: 
    - 3D Printed Shell
        - [x] Rock Mountain Base
        - [ ] I
    - Embedded
        - [ ] main chip
        - [ ] speaker
        - [ ] microphone
        - [ ] LED?
        - [ ] WiFi
        - [ ] control scripts
- Software
    - API
        - [x] ASR
        - [x] TTS
        - [x] OpenAI
    - Scripts
        1. [ ] Receive Audio from I
        2. [ ] ASR to text, text to LLM, get reply, TTS to audio
        3. [ ] Send Audio Back to I


## Software-side Setup
- `conda create -n "terrible" python=3.12`
- `conda activate terrible`
- `pip install requirements.txt`
- `conda install conda-forge::ffmpeg`

### Running APIs
`cd api`

- ASR (audio to text)
    - `python asr.py`
- TTS (text to audio)
    - `python tts.py`

### WebUI for testing
- `cd interface`
- `streamlit run webui.py`

### Available Methods
- LLM
    - `gpt_response`
        - `user_input`: optional question string
        - returns: `prompt`, **`resp_text`** (cleaned response text suitable for TTS)
