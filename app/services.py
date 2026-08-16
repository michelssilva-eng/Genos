import wave
import subprocess

from faster_whisper import WhisperModel
from groq import Groq
from piper import PiperVoice
import imageio_ffmpeg


def sound_to_text(
        model: WhisperModel,
        input_audio_path: str) -> str:
    
    segments, info = model.transcribe(
        input_audio_path,
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

def text_to_sound(
        piper_voice: PiperVoice,
        text: str,
        raw_output_audio_path: str,
        output_audio_path: str):
    
    with wave.open(raw_output_audio_path, "wb") as wav_file:
        piper_voice.synthesize_wav(
            text,
            wav_file,
        )

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    subprocess.run([
        ffmpeg,
        "-y",
        "-i", raw_output_audio_path,
        "-c:a", "libopus",
        "-b:a", "48k",
        output_audio_path,
    ], check=True)

# def text_to_sound(piper_voice: PiperVoice, text: str) -> bytes:
#     wav_buffer = BytesIO()

#     with wave.open(wav_buffer, "wb") as wav_file:
#         piper_voice.synthesize_wav(
#             text,
#             wav_file,
#         )

#     wav_buffer.seek(0)

#     ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

#     result = subprocess.run(
#         [
#             ffmpeg,
#             "-i", "pipe:0",
#             "-c:a", "libopus",
#             "-b:a", "48k",
#             "-f", "ogg",
#             "pipe:1",
#         ],
#         input=wav_buffer.read(),
#         capture_output=True,
#         check=True,
#     )

#     return result.stdout
    
