from abc import ABC, abstractmethod

class SpeechToText(ABC):
    @abstractmethod
    def transcribe(self, audio: bytes) -> str:
        pass