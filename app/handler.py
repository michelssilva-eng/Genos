import io
import logging
import time

from telegram import Update
from telegram.ext import ContextTypes

from service import Service
from engines.exceptions import SpeechToTextError, LanguageModelError, TextToSpeechError


logger = logging.getLogger(__name__)

async def start(
          update: Update,
          _: ContextTypes.DEFAULT_TYPE,
          service: Service):
    
    if not update.message:
        return

    text = "Olá! Me chamo Áisak. Qual é o seu nome?"

    output_audio = service.reply_to_start(text)
    
    audio_file = io.BytesIO(output_audio)
    audio_file.name = "voice.ogg"


    await update.message.reply_voice(
        voice=audio_file
    )


async def reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    service: Service,
):
    if not update.message:
        return

    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    try:
        download_start = time.perf_counter()
        telegram_file = await context.bot.get_file(
            telegram_voice.file_id
        )

        input_audio_bytes = bytes(
            await telegram_file.download_as_bytearray()
        )

        logger.info(
            "Download concluído | tempo=%.2fs",
            time.perf_counter() - download_start,
        )

        service_start = time.perf_counter()
        output_audio = service.reply_to_voice(
            input_audio_bytes
        )

        logger.info(
            "Service concluído | tempo=%.2fs",
            time.perf_counter() - service_start,
        )

    except SpeechToTextError:
        await update.message.reply_text(
            "Não consegui entender o áudio."
        )
        return

    except LanguageModelError:
        await update.message.reply_text(
            "Tive um problema ao processar sua mensagem."
        )
        return

    except TextToSpeechError:
        await update.message.reply_text(
            "Consegui processar sua mensagem, mas não consegui gerar o áudio."
        )
        return

    audio_file = io.BytesIO(output_audio)
    audio_file.name = "voice.ogg"

    send_start = time.perf_counter()
    await update.message.reply_voice(
        voice=audio_file
    )

    logger.info(
        "Envio concluído | tempo=%.2fs",
        time.perf_counter() - send_start,
    )