import io

from telegram import Update
from telegram.ext import ContextTypes

from service import Service


async def start(
          update: Update,
          _: ContextTypes.DEFAULT_TYPE,
          service: Service):
    
    if not update.message:
        return

    text = "Olá! Me chamo Kira. Qual é o seu nome?"

    output_audio = service.reply_to_start(text)
    
    audio_file = io.BytesIO(output_audio)
    audio_file.name = "voice.ogg"


    await update.message.reply_voice(
        voice=audio_file
    )


async def reply(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        service: Service):

    if not update.message:
            return
        
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    telegram_file = await context.bot.get_file(telegram_voice.file_id)

    input_audio = bytes(
            await telegram_file.download_as_bytearray()
        )
    
    output_audio = service.reply_to_voice(input_audio)

    audio_file = io.BytesIO(output_audio)
    audio_file.name = "voice.ogg"


    await update.message.reply_voice(
        voice=audio_file
    )