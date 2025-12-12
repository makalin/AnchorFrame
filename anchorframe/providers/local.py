from .base import BackendProvider
import json
import urllib.request
import urllib.parse

class LocalComfyProvider(BackendProvider):
    """
    The standard local ComfyUI connection.
    Refactored from old ComfyClient.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        
    def queue_prompt(self, workflow: dict) -> str:
        p = {"prompt": workflow}
        data = json.dumps(p).encode('utf-8')
        url = f"{self.base_url}/prompt"
        
        try:
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req) as response:
                resp_data = json.loads(response.read())
                return resp_data.get('prompt_id')
        except Exception as e:
            # Silence expected connection errors in demo mode, or log them
            # print(f"Error queueing prompt: {e}") 
            return None

    def is_reachable(self) -> bool:
        try:
            with urllib.request.urlopen(self.base_url) as response:
                return response.status == 200
        except:
            return False
