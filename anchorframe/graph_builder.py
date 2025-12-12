import json
import uuid

class GraphBuilder:
    """
    Constructs the ComfyUI workflow JSON.
    In a real system, this would be much more complex, potentially loading templates
    or dynamically connecting nodes based on the assets provided.
    """
    def build_workflow(self, components: dict) -> dict:
        """
        Builds a ComfyUI workflow dictionary based on the shot components.
        
        Args:
            components (dict): Contains 'assets', 'scene', 'prompt', 'seed', etc.
        """
        # simplified mock workflow structure
        workflow = {}
        
        # 1. KSampler (The core generation node)
        sampler_id = str(uuid.uuid4())
        workflow[sampler_id] = {
            "inputs": {
                "seed": components.get("seed", 0),
                "steps": 20,
                "cfg": 8.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["MODEL_LOADER_ID", 0],
                "positive": ["POSITIVE_PROMPT_ID", 0],
                "negative": ["NEGATIVE_PROMPT_ID", 0],
                "latent_image": ["EMPTY_LATENT_ID", 0]
            },
            "class_type": "KSampler"
        }

        # 2. Prompts
        pos_id = "POSITIVE_PROMPT_ID"
        workflow[pos_id] = {
            "inputs": {"text": components.get("prompt", "") + ", highest quality"},
            "class_type": "CLIPTextEncode"
        }
        
        neg_id = "NEGATIVE_PROMPT_ID"
        workflow[neg_id] = {
            "inputs": {"text": "text, watermark, bad quality"},
            "class_type": "CLIPTextEncode"
        }

        # 3. Connect Assets (Mock IP-Adapter Injection)
        # In a real graph, we would loop through components['assets'] and add IPAdapter nodes
        # linked to the model input of the KSampler.
        
        # 4. Connect Scene (Mock ControlNet Injection)
        # Similarly, we would add ControlNetApply nodes linked to the positive conditioning.
        
        # 5. Save Image
        save_id = "SAVE_IMAGE_ID"
        workflow[save_id] = {
            "inputs": {"filename_prefix": "AnchorFrame_Helpers"},
            "class_type": "SaveImage"
        }
        
        return workflow
