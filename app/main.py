from functools import partial

from faster_whisper import WhisperModel
from piper import PiperVoice
from groq import Groq
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


from settings import VOICE_PATH, GROQ_KEY, TELEGRAM_TOKEN, CORRECTION_PROMPT
from handlers import start, echo_in_text, reply

from ports.stt.adapters.faster_whisper import FasterWhisper
from ports.tts.adapters.piper import Piper
from ports.llm.adapters.groq import GroqLLM


def main():

    # sound-to-text
    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8",
    )

    stt = FasterWhisper(model=model)

    # llm
    client = Groq(
            api_key=GROQ_KEY
        )

    llm = GroqLLM(client=client)


    # text-to-sound
    piper_voice = PiperVoice.load(VOICE_PATH)

    tts = Piper(voice=piper_voice)

    # bot telegram
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # app.add_handler(MessageHandler(
    #     filters.VOICE,
    #     partial(echo_in_text,
    #             model=model,
    #             client=client,
    #             input_audio_path=INPUT_AUDIO_PATH,
    #             correction_prompt=CORRECTION_PROMPT)))
    
    app.add_handler(MessageHandler(
        filters.VOICE,
        partial(
            reply,
            stt=stt,
            llm=llm,
            tts=tts,
            correction_prompt=CORRECTION_PROMPT)))

    
    app.run_polling()

if __name__ == "__main__":
    main()