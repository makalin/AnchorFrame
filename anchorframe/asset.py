import os

class Asset:
    """
    Represents a character or object that needs to be consistent across shots.
    In a real implementation, this would handle computing embeddings from the source image.
    """
    def __init__(self, name: str, image_path: str, type: str = "person"):
        self.name = name
        self.image_path = image_path
        self.type = type
        self.embedding = None # Placeholder for cached embedding

        if not os.path.exists(image_path):
            print(f"Warning: Asset image not found at {image_path}")

    def __repr__(self):
        return f"Asset(name='{self.name}', type='{self.type}')"
