class EngineError(Exception):
    """Base para erros relacionados aos engines."""


class SpeechToTextError(EngineError):
    """Erro durante a transcrição de áudio."""


class TextToSpeechError(EngineError):
    """Erro durante a síntese de áudio."""


class LanguageModelError(EngineError):
    """Erro durante a geração de texto."""