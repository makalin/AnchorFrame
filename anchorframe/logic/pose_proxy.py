from PIL import Image, ImageDraw

class PoseProxy:
    """
    Generates synthetic OpenPose-style stick figure images.
    Useful for programmatic blocking without needing real reference pose images.
    """
    def __init__(self):
        pass

    def create_pose(self, width: int = 512, height: int = 512, keypoints: dict = None) -> Image.Image:
        """
        Creates a black image with OpenPose-colored limbs drawn.
        
        Colors (approximate OpenPose standard):
        - Nose: (0, 0, 255) (not implemented for stick)
        - Body: (255, 0, 0)
        - Arms: varying
        
        Args:
            keypoints (dict): Just a placeholder for now.
             In a real implementation this would take explicit (x,y) coords.
        """
        img = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a dummy "T-Pose" or "Standing" figure if no keypoints
        # Center x, y
        cx, cy = width // 2, height // 2
        
        # Torso
        draw.line((cx, cy - 100, cx, cy + 50), fill=(0, 0, 255), width=10) # Body (Blue-ish in some schemes, standardizing on visible colors)
        
        # Neck to Head
        draw.line((cx, cy - 100, cx, cy - 150), fill=(255, 0, 0), width=10)
        draw.ellipse((cx - 20, cy - 190, cx + 20, cy - 150), fill=(255, 0, 0)) # Head
        
        # Arms
        draw.line((cx, cy - 100, cx - 80, cy - 80), fill=(50, 255, 50), width=10) # Left Arm
        draw.line((cx, cy - 100, cx + 80, cy - 80), fill=(50, 255, 50), width=10) # Right Arm
        
        # Legs
        draw.line((cx, cy + 50, cx - 40, cy + 200), fill=(255, 100, 0), width=10) # Left Leg
        draw.line((cx, cy + 50, cx + 40, cy + 200), fill=(255, 100, 0), width=10) # Right Leg
        
        return img
