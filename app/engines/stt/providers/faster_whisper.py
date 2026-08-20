from io import BytesIO

from faster_whisper import WhisperModel

from ..interface import SpeechToText
from ...exceptions import SpeechToTextError


class FasterWhisper(SpeechToText):

    def __init__(self, model: WhisperModel) -> None:
        self.model = model

    def transcribe(self, audio: bytes) -> str:
        try:
            segments, _ = self.model.transcribe(
                BytesIO(audio),
                language="pt",
            )

            text = "".join(segment.text for segment in segments)

            if not text.strip():
                raise SpeechToTextError(
                    "Nenhuma palavra foi identificada."
                )

            return text

        except SpeechToTextError:
            raise

        except Exception as error:
            raise SpeechToTextError(
                "Não foi possível transcrever o áudio."
            ) from error

        