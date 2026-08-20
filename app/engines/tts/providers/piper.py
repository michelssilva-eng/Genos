import wave
from io import BytesIO
import subprocess

from piper import PiperVoice
import imageio_ffmpeg

from ..interface import TextToSpeech
from ...exceptions import TextToSpeechError


class Piper(TextToSpeech):
    def __init__(self, voice: PiperVoice) -> None:
        self.voice = voice

    def synthesize(self, text: str) -> bytes:
        try:

            text = self._normalize(text=text)

            wav_buffer = BytesIO()

            with wave.open(wav_buffer, "wb") as wav_file:
                self.voice.synthesize_wav(
                    text,
                    wav_file,
                )

            wav_buffer.seek(0)

            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
            
            result = subprocess.run(
                [
                    ffmpeg,
                    "-loglevel", "error",
                    "-i", "pipe:0",
                    "-c:a", "libopus",
                    "-b:a", "48k",
                    "-f", "ogg",
                    "pipe:1",
                ],
                input=wav_buffer.getvalue(),
                capture_output=True,
                check=True,
            )

            return result.stdout

        except TextToSpeechError:
                    raise

        except Exception as error:
            raise TextToSpeechError(
                "Falha ao sintetizar o áudio."
            ) from error