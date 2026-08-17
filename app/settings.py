import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env(name: str) -> str:
  """Busca uma variável de ambiente e garante que ela não é None."""
  value = os.getenv(name)
  if value is None:
    raise ValueError(f"Erro: A variável de ambiente '{name}' não foi definida.")
  return value

GROQ_KEY = get_required_env("GROQ_KEY")
TELEGRAM_TOKEN = get_required_env("TELEGRAM_TOKEN")

VOICE_PATH = "app/voices/pt_BR-cadu-medium.onnx"

CORRECTION_PROMPT = f"""
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

"""