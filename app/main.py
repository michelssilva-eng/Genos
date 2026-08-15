from faster_whisper import WhisperModel
from piper import PiperVoice
from groq import Groq
import imageio_ffmpeg
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from functools import partial

from settings import VOICE_PATH, GROQ_KEY, TELEGRAM_TOKEN
from handlers import start, echo


def main():

    # sound-to-text
    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8",
    )

    # llm
    client = Groq(
            api_key=GROQ_KEY
        )

    # text-to-sound
    piper_voice = PiperVoice.load(VOICE_PATH)

    
    # .wav to .ogg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    # bot telegram
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, partial(echo, model=model, client=client)))
    app.run_polling()

if __name__ == "__main__":
    main()