import wave

from piper import PiperVoice

voice = PiperVoice.load("pt_BR-cadu-medium.onnx")

with wave.open("resposta.wav", "wb") as wav_file:
    voice.synthesize_wav(
        "Olá, Michel. Eu sou seu assistente.",
        wav_file,
    )