from groq import Groq

from ..interface import LanguageModel
from ...exceptions import LanguageModelError


class GroqLLM(LanguageModel):
    def __init__(self, client: Groq) -> None:
        self.client = client

    def generate(self, prompt: str) -> str:
        try:
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
                raise LanguageModelError(
                    "O modelo não retornou uma resposta."
                )

            return text

        except LanguageModelError:
            raise

        except Exception as error:
            raise LanguageModelError(
                "Falha ao gerar resposta com o modelo."
            ) from error