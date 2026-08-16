from faster_whisper import WhisperModel
from groq import Groq
from piper import PiperVoice
import wave
import subprocess

import imageio_ffmpeg


from settings import INPUT_AUDIO_PATH, CORRECTION_PROMPT, RAW_OUTPUT_AUDIO_PATH, OUTPUT_AUDIO_PATH

def sound_to_text(model: WhisperModel) -> str:
    segments, info = model.transcribe(
        INPUT_AUDIO_PATH,
        language="pt",
    )

    text = ""
        
    for segment in segments:
        text += segment.text

    if text == "":
        raise ValueError("Erro: Nenhuma palavra foi identificiada.")

    return text

def correct_text(client: Groq, text: str) -> str:

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": CORRECTION_PROMPT + text,
            }
        ],
        model="openai/gpt-oss-20b",
    )

    correct_text = chat_completion.choices[0].message.content

    if not correct_text or correct_text == "":
        raise ValueError("Erro: A chamada de correção à LLM respondeu de forma inesperada.")

    return correct_text

def consult_ai(client: Groq, text: str) -> str:

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="openai/gpt-oss-20b",
    )

    ai_response = chat_completion.choices[0].message.content

    if not ai_response or ai_response == "":
        raise ValueError("Erro: A chamada de correção à LLM respondeu de forma inesperada.")

    return ai_response

def text_to_sound(piper_voice: PiperVoice, text: str):
    with wave.open(RAW_OUTPUT_AUDIO_PATH, "wb") as wav_file:
        piper_voice.synthesize_wav(
            text,
            wav_file,
        )

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    subprocess.run([
        ffmpeg,
        "-i", RAW_OUTPUT_AUDIO_PATH,
        "-c:a", "libopus",
        "-b:a", "48k",
        OUTPUT_AUDIO_PATH,
    ], check=True)
    
