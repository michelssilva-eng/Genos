from functools import partial

from faster_whisper import WhisperModel
from piper import PiperVoice
from groq import Groq
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from ports.stt.adapters.faster_whisper import FasterWhisper
from ports.tts.adapters.piper import Piper
from ports.llm.adapters.groq import GroqLLM

from handlers import start, reply
from service import Service

from settings import VOICE_PATH, GROQ_KEY, TELEGRAM_TOKEN


def main():

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8",
    )

    client = Groq(
                api_key=GROQ_KEY
            )

    piper_voice = PiperVoice.load(VOICE_PATH)

    
    stt = FasterWhisper(model=model)
    llm = GroqLLM(client=client)
    tts = Piper(voice=piper_voice)


    service = Service(
        stt=stt,
        tts=tts,
        llm=llm
    )


    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler(
        "start",
        partial(
            start,
            service=service
        )
    ))
    
    
    app.add_handler(MessageHandler(
        filters.VOICE,
        partial(
            reply,
            service=service)))

    
    app.run_polling()

if __name__ == "__main__":
    main()