from ports.stt.interface import SpeechToText
from ports.tts.interface import TextToSpeech
from ports.llm.interface import LanguageModel

from prompts import CORRECTION_PROMPT, VOICE_RESPONSE_PROMPT


class Service:
    def __init__(
            self,
            stt: SpeechToText,
            tts: TextToSpeech,
            llm: LanguageModel
    ) -> None:
        self.stt = stt
        self.tts = tts
        self.llm = llm


    def reply_to_voice(self, input_audio: bytes) -> bytes:
        text = self.stt.transcribe(input_audio)

        corrected_text = self.llm.generate(CORRECTION_PROMPT + text)

        ai_response = self.llm.generate(VOICE_RESPONSE_PROMPT  + corrected_text)

        return self.tts.synthesize(ai_response)

    
    def reply_to_start(self, text: str) -> bytes:
        return self.tts.synthesize(text)