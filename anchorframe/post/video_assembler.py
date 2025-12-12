import cv2
import os
import glob
from typing import Optional

class VideoAssembler:
    """
    Stitches a sequence of images into a video file.
    """
    def __init__(self, fps: int = 24):
        self.fps = fps

    def make_video(self, source_dir: str, output_path: str, file_pattern: str = "*.png"):
        """
        Reads images from source_dir matching file_pattern and writes a video to output_path.
        """
        files = glob.glob(os.path.join(source_dir, file_pattern))
        if not files:
            print(f"No images found in {source_dir} matching {file_pattern}")
            return
            
        # Sort files to ensure order
        files.sort()
        
        # Read first frame to get size
        frame0 = cv2.imread(files[0])
        if frame0 is None:
             print(f"Error reading first frame: {files[0]}")
             return
             
        height, width, layers = frame0.shape
        size = (width, height)
        
        # Initialize VideoWriter
        # 'mp4v' for .mp4 usually works
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, size)
        
        print(f"Assembling video from {len(files)} frames...")
        for filename in files:
            img = cv2.imread(filename)
            if img is not None:
                out.write(img)
            else:
                print(f"Warning: Could not read {filename}")
        
        out.release()
        print(f"Video saved to: {output_path}")
