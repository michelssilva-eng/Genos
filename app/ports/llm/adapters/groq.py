from groq import Groq

from ..interface import LanguageModel


class GroqLLM(LanguageModel):
    def __init__(self, client: Groq) -> None:
        self.client = client

    def generate(self, prompt: str) -> str:

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-20b",
        )

        text = chat_completion.choices[0].message.content

        if not text or not text.strip():
            raise ValueError("Erro: A chamada de correção à LLM respondeu de forma inesperada.")

        return text