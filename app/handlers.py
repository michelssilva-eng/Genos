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
        client: Groq):

    if not update.message:
        return
    
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    # baixando arquivo de áudio
    telegram_file = await context.bot.get_file(telegram_voice.file_id)
    await telegram_file.download_to_drive(INPUT_AUDIO_PATH)

    text_input_audio = sound_to_text(model=model)

    corrected_input_text = correct_text(client=client, text=text_input_audio)

    await update.message.reply_text("Sem correção: " + text_input_audio)
    await update.message.reply_text("Com correção: " + corrected_input_text)


async def reply(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        model: WhisperModel,
        client: Groq,
        piper_voice: PiperVoice):

    if not update.message:
            return
        
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    # baixando arquivo de áudio
    telegram_file = await context.bot.get_file(telegram_voice.file_id)
    await telegram_file.download_to_drive(INPUT_AUDIO_PATH)

    # pegando texto do audio
    text_input_audio = sound_to_text(model=model)

    # corrigindo com llm
    corrected_input_text = correct_text(client=client, text=text_input_audio)

    # resposta da llm
    ai_response = consult_ai(client=client, text=corrected_input_text)

    # gerando audio da resposta
    text_to_sound(piper_voice=piper_voice, text=ai_response)

    # enviando
    await update.message.reply_voice(
            voice=open(OUTPUT_AUDIO_PATH, "rb")
        )