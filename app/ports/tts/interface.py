from abc import ABC, abstractmethod
import re
import unicodedata


class TextToSpeech(ABC):

    def _normalize(self, text: str) -> str:
    # Remove emojis e outros símbolos pictográficos.
        text = "".join(
            char
            for char in text
            if not unicodedata.category(char).startswith("So")
        )

        # Remove Markdown básico.
        text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
        text = re.sub(r"(?<!\w)([*_])(.*?)(?<!\w)\1", r"\2", text)
        text = re.sub(r"`([^`]*)`", r"\1", text)

        # Remove títulos Markdown.
        text = re.sub(r"^\s*#+\s*", "", text, flags=re.MULTILINE)

        # Remove marcadores de listas.
        text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)

        # Remove excesso de espaços.
        text = re.sub(r"[ \t]+", " ", text)

        # Normaliza quebras de linha.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        pass