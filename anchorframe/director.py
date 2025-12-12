from typing import List, Optional
import os
from .asset import Asset
from .scene import Scene
from .graph_builder import GraphBuilder
from .post.video_assembler import VideoAssembler
from .utils.logger import configure_logger

from .providers import BackendProvider, LocalComfyProvider
from .audio import TTSProvider, ElevenLabsProvider, AudioSync, Wav2LipSync

from dotenv import load_dotenv

class Director:
    """
    The main coordinator class.
    """
    def __init__(self, project: str, provider: BackendProvider = None):
        load_dotenv()
        self.logger = configure_logger()
        self.project = project
        
        # Use provided provider or default to Local
        if provider:
            self.client = provider
        else:
            comfy_url = os.getenv("COMFY_UI_URL", "http://127.0.0.1:8188")
            self.client = LocalComfyProvider(comfy_url)
            
        self.output_dir = os.getenv("OUTPUT_DIR", "./renders")
        
        # Modules
        self.builder = GraphBuilder()
        self.assembler = VideoAssembler()
        self.tts = ElevenLabsProvider() # Default
        self.sync = Wav2LipSync()       # Default
        
        self.shots = []
        
        self.logger.info(f"Director initialized for project: {self.project}")
        self.logger.info(f"Backend Reachable: {self.client.is_reachable()}")

    def shoot(self, assets: List[Asset], scene: Scene, prompt: str, frames: int = 24, motion_strength: float = 0.5, seed: int = 0, audio_text: str = None):
        """
        Registers a shot to be filmed.
        """
        # 1. Generate Audio if needed
        audio_path = None
        if audio_text:
            filename = f"audio_{len(self.shots)}.mp3"
            os.makedirs(self.output_dir, exist_ok=True)
            audio_path = os.path.join(self.output_dir, filename)
            self.tts.generate_audio(audio_text, "voice_01", audio_path)
            self.logger.info(f"Generated audio line: '{audio_text}'")

        shot_metadata = {
            "assets": assets,
            "scene": scene,
            "prompt": prompt,
            "frames": frames,
            "motion_strength": motion_strength,
            "seed": seed,
            "audio_path": audio_path
        }
        self.shots.append(shot_metadata)
        self.logger.info(f"Shot scheduled: '{prompt[:30]}...' (Audio: {bool(audio_path)})")

    def action(self):
        """
        Triggers the generation for all scheduled shots.
        """
        self.logger.info(f"ACTION! Processing {len(self.shots)} shots...")
        
        for i, shot in enumerate(self.shots):
            self.logger.info(f"Processing Shot {i+1}...")
            # 1. Build workflow
            workflow = self.builder.build_workflow(shot)
            
            # 2. Queue Prompt
            prompt_id = self.client.queue_prompt(workflow)
            
            if prompt_id:
                self.logger.info(f"Shot {i+1} queued! ID: {prompt_id}")
            else:
                self.logger.error(f"Shot {i+1} failed to queue.")
            
            # 3. Audio Sync (Mock)
            if shot.get('audio_path'):
                # In real life, we would wait for the video generation to finish first
                video_filename = f"AnchorFrame_Helpers_{i+1:05d}_.png" # hypothetical
                # self.sync.sync_video(video_filename, shot['audio_path'], ...)
                self.logger.info(f"Syncing audio {shot['audio_path']} to shot...")
        
        self.logger.info("That's a wrap! (Check ComfyUI implementation for outputs)")
