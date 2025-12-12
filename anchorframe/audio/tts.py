from abc import ABC, abstractmethod
import os

class TTSProvider(ABC):
    @abstractmethod
    def generate_audio(self, text: str, voice_id: str, output_path: str):
        pass

class ElevenLabsProvider(TTSProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ELEVEN_LABS_API_KEY")

    def generate_audio(self, text: str, voice_id: str, output_path: str):
        # Mock implementation for demo
        print(f"[ElevenLabs] Generating audio for '{text[:20]}...' with voice {voice_id}")
        # In real life, request API and save MP3
        # Creating a dummy file
        with open(output_path, 'w') as f:
            f.write("dummy audio content")
