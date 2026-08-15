from faster_whisper import WhisperModel
from groq import Groq

from settings import INPUT_AUDIO_PATH, CORRECTION_PROMPT

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

