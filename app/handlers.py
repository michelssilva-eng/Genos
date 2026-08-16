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
        input_audio_path: str,
        correction_prompt: str
        ):

    if not update.message:
        return
    
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    # baixando arquivo de áudio
    telegram_file = await context.bot.get_file(telegram_voice.file_id)
    await telegram_file.download_to_drive(input_audio_path)

    text_input_audio = sound_to_text(model=model, input_audio_path=input_audio_path)

    corrected_input_text = correct_text(client=client, text=text_input_audio, correction_prompt=correction_prompt)

    await update.message.reply_text("Sem correção: " + text_input_audio)
    await update.message.reply_text("Com correção: " + corrected_input_text)


async def reply(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        model: WhisperModel,
        client: Groq,
        piper_voice: PiperVoice,
        input_audio_path: str,
        correction_prompt: str,
        raw_output_audio_path: str,
        output_audio_path: str
        ):

    if not update.message:
            return
        
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    # baixando arquivo de áudio
    telegram_file = await context.bot.get_file(telegram_voice.file_id)
    await telegram_file.download_to_drive(input_audio_path)

    # pegando texto do audio
    text_input_audio = sound_to_text(model=model, input_audio_path=input_audio_path)

    # corrigindo com llm
    corrected_input_text = correct_text(client=client, text=text_input_audio, correction_prompt=correction_prompt)

    # resposta da llm
    ai_response = consult_ai(client=client, text=corrected_input_text)

    # gerando audio da resposta
    text_to_sound(piper_voice=piper_voice, text=ai_response, raw_output_audio_path=raw_output_audio_path, output_audio_path=output_audio_path)

    # enviando
    await update.message.reply_voice(
            voice=open(output_audio_path, "rb")
        )