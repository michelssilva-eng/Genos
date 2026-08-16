from time import perf_counter
import io

from telegram import Update
from telegram.ext import ContextTypes
from faster_whisper import WhisperModel
from groq import Groq
from piper import PiperVoice

from settings import INPUT_AUDIO_PATH, OUTPUT_AUDIO_PATH
from services import sound_to_text, correct_text, consult_ai, text_to_sound


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text("Olá! Me chamo Genos.")


async def echo_in_text(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        model: WhisperModel,
        client: Groq,
        correction_prompt: str
        ):

    started_at = perf_counter()

    if not update.message:
        return
    
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    # baixando arquivo de áudio
    telegram_file = await context.bot.get_file(telegram_voice.file_id)

    audio_bytes = bytes(
        await telegram_file.download_as_bytearray()
    )

    text_input_audio = sound_to_text(model=model, audio_bytes=audio_bytes)

    corrected_input_text = correct_text(client=client, text=text_input_audio, correction_prompt=correction_prompt)

    finished_at = perf_counter()

    await update.message.reply_text(f"Texto obitido: '{text_input_audio}'\nTexto corrigido: '{corrected_input_text}'\nTempo: {finished_at - started_at}s")


async def reply(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        model: WhisperModel,
        client: Groq,
        piper_voice: PiperVoice,
        correction_prompt: str):

    started_at = perf_counter()

    if not update.message:
            return
        
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    # baixando arquivo de áudio
    telegram_file = await context.bot.get_file(telegram_voice.file_id)

    input_audio_bytes = bytes(
            await telegram_file.download_as_bytearray()
        )
    
    # await telegram_file.download_to_drive(input_audio_path)

    # pegando texto do audio
    text_input_audio = sound_to_text(model=model, audio_bytes=input_audio_bytes)

    # corrigindo com llm
    corrected_input_text = correct_text(
         client=client,
         text=text_input_audio,
         correction_prompt=correction_prompt)

    # resposta da llm
    ai_response = consult_ai(client=client, text=corrected_input_text)

    # gerando audio da resposta
    output_audio_bytes = text_to_sound(
         piper_voice=piper_voice,
         text=ai_response)

    # preparando para envio
    audio_file = io.BytesIO(output_audio_bytes)
    audio_file.name = "voice.ogg"

    # enviando
    await update.message.reply_voice(
        voice=audio_file
    )

    finished_at = perf_counter()

    await update.message.reply_text(
         f"Tempo de resposta: {finished_at - started_at}s"
    )