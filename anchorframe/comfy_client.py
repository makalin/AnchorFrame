import json
import urllib.request
import urllib.parse
import time

class ComfyClient:
    """
    Handles communication with the ComfyUI HTTP API.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def queue_prompt(self, prompt_workflow: dict) -> str:
        """
        Sends the workflow to ComfyUI for generation.
        Returns the prompt_id.
        """
        p = {"prompt": prompt_workflow}
        data = json.dumps(p).encode('utf-8')
        url = f"{self.base_url}/prompt"
        
        try:
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req) as response:
                resp_data = json.loads(response.read())
                return resp_data.get('prompt_id')
        except Exception as e:
            print(f"Error queueing prompt: {e}")
            return None

    def get_history(self, prompt_id: str) -> dict:
        """
        Retrieves the history for a specific prompt_id to check for outputs.
        """
        url = f"{self.base_url}/history/{prompt_id}"
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read())
        except Exception as e:
            print(f"Error getting history: {e}")
            return {}

    def is_reachable(self) -> bool:
        """
        Simple check to see if the server is up.
        """
        try:
            with urllib.request.urlopen(self.base_url) as response:
                return response.status == 200
        except:
            return False
