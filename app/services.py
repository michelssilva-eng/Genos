import wave
import subprocess
import io

from faster_whisper import WhisperModel
from groq import Groq
from piper import PiperVoice
import imageio_ffmpeg


def sound_to_text(
        model: WhisperModel,
        audio_bytes: bytes) -> str:

    audio_file = io.BytesIO(audio_bytes)
    
    segments, info = model.transcribe(
        audio_file,
        language="pt",
    )

    text = "".join(segment.text for segment in segments)

    if not text.strip():
        raise ValueError("Erro: Nenhuma palavra foi identificiada.")

    return text

def correct_text(
        client: Groq,
        text: str,
        correction_prompt: str) -> str:

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": correction_prompt + text,
            }
        ],
        model="openai/gpt-oss-20b",
    )

    corrected_text = chat_completion.choices[0].message.content

    if not corrected_text or corrected_text == "":
        raise ValueError("Erro: A chamada de correção à LLM respondeu de forma inesperada.")

    return corrected_text

def consult_ai(
        client: Groq,
        text: str) -> str:

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

def text_to_sound(piper_voice: PiperVoice, text: str) -> bytes:
    wav_buffer = io.BytesIO()

    with wave.open(wav_buffer, "wb") as wav_file:
        piper_voice.synthesize_wav(
            text,
            wav_file,
        )

    wav_buffer.seek(0)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    result = subprocess.run(
        [
            ffmpeg,
            "-loglevel", "error",
            "-i", "pipe:0",
            "-c:a", "libopus",
            "-b:a", "48k",
            "-f", "ogg",
            "pipe:1",
        ],
        input=wav_buffer.getvalue(),
        capture_output=True,
        check=True,
    )

    return result.stdout
    
