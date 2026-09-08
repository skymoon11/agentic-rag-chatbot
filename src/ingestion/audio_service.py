import os

from deepgram import DeepgramClient
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


def transcribe_audio(file_path: str) -> str:
    """Transcribe an audio file (mp3, wav, or m4a) using Deepgram Nova-2."""
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY is not set in environment variables.")

    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    with open(file_path, "rb") as audio:
        response = deepgram.listen.v1.media.transcribe_file(
            request=audio.read(),
            model="nova-2",
            smart_format=True,
            punctuate=True,
            language="en",
        )

    return response.results.channels[0].alternatives[0].transcript