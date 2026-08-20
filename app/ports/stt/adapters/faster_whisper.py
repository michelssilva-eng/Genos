from io import BytesIO

from faster_whisper import WhisperModel

from ..interface import SpeechToText




class FasterWhisper(SpeechToText):
    def __init__(self, model: WhisperModel) -> None:
        self.model = model

    def transcribe(self, audio: bytes) -> str:

        segments, _ = self.model.transcribe(
                    BytesIO(audio),
                    language="pt",
                )

        text = "".join(segment.text for segment in segments)
        
        if not text.strip():
            raise ValueError("Erro: Nenhuma palavra foi identificiada.")

        return text