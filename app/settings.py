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

VOICE_PATH = "app/voices/pt_BR-faber-medium.onnx"