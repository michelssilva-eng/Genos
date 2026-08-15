from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from faster_whisper import WhisperModel
import wave
from piper import PiperVoice
import subprocess
import imageio_ffmpeg
from groq import Groq


piper_voice = PiperVoice.load("pt_BR-cadu-medium.onnx")
TOKEN = "8505771374:AAEZPiKb3eMUIjwqdjDe0WqYWq9yipBs8b0"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)

client = Groq(
    api_key="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"  # This is the default and can be omitted
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text("Olá! Eu estou funcionando.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    telegram_file = await context.bot.get_file(telegram_voice.file_id)

    await telegram_file.download_to_drive("input_audio.ogg")

    segments, info = model.transcribe(
        "input_audio.ogg",
        language="pt",
    )

    text = ""

    for segment in segments:
        text += segment.text


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="openai/gpt-oss-20b",
    )

    if not chat_completion.choices[0].message.content:
        return

    with wave.open("resposta.wav", "wb") as wav_file:
        piper_voice.synthesize_wav(
            chat_completion.choices[0].message.content,
            wav_file,
        )

    subprocess.run([
        ffmpeg,
        "-y",
        "-i", "resposta.wav",
        "-c:a", "libopus",
        "-b:a", "48k",
        "output_audio.ogg",
    ], check=True)

    await update.message.reply_text(text)

    await update.message.reply_voice(
        voice=open("output_audio.ogg", "rb")
    )



def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, echo))

    app.run_polling()


if __name__ == "__main__":
    main()