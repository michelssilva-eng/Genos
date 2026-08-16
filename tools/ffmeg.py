import subprocess

import imageio_ffmpeg


ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

subprocess.run([
    ffmpeg,
    "-i", "resposta.wav",
    "-c:a", "libopus",
    "-b:a", "48k",
    "resposta_ouvivel.ogg",
], check=True)