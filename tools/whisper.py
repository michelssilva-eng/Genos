from faster_whisper import WhisperModel

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8",
)

segments, info = model.transcribe(
    "input_audio.ogg",
    language="pt",
)

text = ""

for segment in segments:
    text += segment.text

print(text)