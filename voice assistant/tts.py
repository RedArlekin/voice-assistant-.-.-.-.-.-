import torch
import sounddevice as sd
import time

language = 'ru'
model_id = 'v4_ru'
sample_rate = 48000 # 48000
speaker = 'baya' # aidar, baya, kseniya, xenia, eugene, random
put_accent = True
put_yo = True
device = torch.device('cpu') # cpu или gpu
text = "Привет, МИР!!"

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)


def va_speak(what: str):
    audio = model.apply_tts(text=what,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio, sample_rate)
    sd.wait()
    sd.stop()

va_speak(text)