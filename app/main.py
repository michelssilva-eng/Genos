from functools import partial

from faster_whisper import WhisperModel
from piper import PiperVoice
from groq import Groq
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from settings import VOICE_PATH, GROQ_KEY, TELEGRAM_TOKEN, INPUT_AUDIO_PATH, CORRECTION_PROMPT, RAW_OUTPUT_AUDIO_PATH, OUTPUT_AUDIO_PATH
from handlers import start, echo_in_text, reply


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


    # bot telegram
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # app.add_handler(MessageHandler(filters.VOICE, partial(echo, model=model, client=client)))
    app.add_handler(MessageHandler(
        filters.VOICE,
        partial(
            reply,
            model=model,
            client=client,
            piper_voice=piper_voice,
            input_audio_path=INPUT_AUDIO_PATH,
            correction_prompt=CORRECTION_PROMPT,
            raw_output_audio_path=RAW_OUTPUT_AUDIO_PATH,
            output_audio_path=OUTPUT_AUDIO_PATH)))

    
    app.run_polling()

if __name__ == "__main__":
    main()