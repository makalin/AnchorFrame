import os

class Scene:
    """
    Represents the background or environment for a shot.
    Can be locked (static camera) or allow for movement.
    """
    def __init__(self, image_path: str, lock_camera: bool = True):
        self.image_path = image_path
        self.lock_camera = lock_camera
        
        if not os.path.exists(image_path):
            print(f"Warning: Scene image not found at {image_path}")

    def __repr__(self):
        return f"Scene(image_path='{self.image_path}', lock_camera={self.lock_camera})"
