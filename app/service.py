import logging

from engines.stt.interface import SpeechToText
from engines.tts.interface import TextToSpeech
from engines.llm.interface import LanguageModel

from prompts import CORRECTION_PROMPT, VOICE_RESPONSE_PROMPT


logger = logging.getLogger(__name__)

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

        logger.info("STT")
        text = self.stt.transcribe(input_audio)

        logger.info("LLM correction")
        corrected_text = self.llm.generate(CORRECTION_PROMPT + text)

        logger.info("LLM response")
        ai_response = self.llm.generate(VOICE_RESPONSE_PROMPT  + corrected_text)

        logger.info("TTS")
        output_audio = self.tts.synthesize(ai_response)

        return output_audio

    
    def reply_to_start(self, text: str) -> bytes:
        return self.tts.synthesize(text)