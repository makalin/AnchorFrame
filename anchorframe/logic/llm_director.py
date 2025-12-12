from typing import List, Dict
import re

class LLMDirector:
    """
    Parses a screenplay-like text into structured shot metadata.
    In a full version, this would use OpenAI API to interpret complex scenes.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def convert_script(self, script_text: str) -> List[Dict]:
        """
        Parses a script into a list of shot definitions.
        
        Supported Format:
        [SCENE_EXT_BRIDGE]
        HERO: "Hello world" (Action: waving hand)
        """
        shots = []
        
        # Simple Mock Parser
        lines = script_text.split('\n')
        current_scene = "default_scene"
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            if line.startswith('[') and line.endswith(']'):
                current_scene = line[1:-1]
                continue
                
            # Regex for DIALOGUE: CHARACTER: "Text" (Action: ...)
            match = re.search(r'(\w+):\s*"(.*?)"\s*\(Action:\s*(.*?)\)', line)
            
            if match:
                character = match.group(1)
                dialogue = match.group(2)
                action = match.group(3)
                
                shot = {
                    "scene_id": current_scene,
                    "character": character,
                    "dialogue": dialogue,
                    "action": action,
                    "prompt": f"{character} {action}, {current_scene}, cinematic lighting"
                }
                shots.append(shot)
            else:
                # Fallback for non-dialogue lines
                pass
                
        return shots
