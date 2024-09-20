from TTS.api import TTS

# Download the model ahead of time
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)