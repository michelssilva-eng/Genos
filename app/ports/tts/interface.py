from abc import ABC, abstractmethod

class TextToSpeech(ABC):

    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        pass