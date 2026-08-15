from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from faster_whisper import WhisperModel

from groq import Groq


TOKEN = "8505771374:AAEZPiKb3eMUIjwqdjDe0WqYWq9yipBs8b0"

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)

client = Groq(
    api_key="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"  # This is the default and can be omitted
)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
            return
    telegram_voice = update.message.voice

    if not telegram_voice:
        return

    # baixando arquivo
    telegram_file = await context.bot.get_file(telegram_voice.file_id)

    await telegram_file.download_to_drive("input_audio.ogg")

    # audio -> texto
    segments, info = model.transcribe(
            "input_audio.ogg",
            language="pt",
        )

    text = ""
    
    for segment in segments:
        text += segment.text

    #

    prompt = f"""
Você é um corretor de transcrições de áudio.

Sua tarefa é corrigir erros de transcrição, mantendo exatamente o significado e a intenção do texto original.

Regras:
- Corrija erros ortográficos e palavras claramente transcritas incorretamente.
- Corrija pontuação quando necessário.
- Não adicione informações.
- Não remova informações.
- Não reformule frases desnecessariamente.
- Não altere nomes próprios sem evidência suficiente.
- Preserve números, datas, nomes e termos técnicos.
- Se uma palavra parecer estranha, mas puder ser intencional, mantenha-a.
- Se a transcrição já estiver correta, retorne-a sem alterações.
- Retorne SOMENTE a transcrição corrigida, sem explicações, aspas ou comentários.

Transcrição:
{text}

"""

    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-20b",
        )

    if not chat_completion.choices[0].message.content:
            return

    correct_text = chat_completion.choices[0].message.content

    await update.message.reply_text("Sem correção:" + text)
    await update.message.reply_text("Com correção: "+ correct_text)



def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.VOICE, echo))

    app.run_polling()


if __name__ == "__main__":
    main()