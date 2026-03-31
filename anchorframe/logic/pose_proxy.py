from PIL import Image, ImageDraw
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

class PoseProxy:
    """
    Generates synthetic OpenPose-style stick figure images.
    Useful for programmatic blocking without needing real reference pose images.
    """
    def __init__(self):
        pass

    def create_pose(
        self,
        width: int = 512,
        height: int = 512,
        keypoints: dict = None,
        preset: str = "standing",
        stroke: int = 10,
    ) -> Image.Image:
        """
        Creates a black image with OpenPose-colored limbs drawn.

        - If `keypoints` is provided, it should be a dict of named points -> (x, y) in pixels.
        - Otherwise a simple preset pose is drawn.
        """
        if keypoints:
            return self.create_pose_from_keypoints(width, height, keypoints=keypoints, stroke=stroke)
        return self.create_preset(width, height, preset=preset, stroke=stroke)

    def create_preset(self, width: int, height: int, preset: str = "standing", stroke: int = 10) -> Image.Image:
        img = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        cx, cy = width // 2, height // 2

        presets = {
            "standing": {
                "head": (cx, cy - 170),
                "neck": (cx, cy - 120),
                "hip": (cx, cy + 40),
                "l_shoulder": (cx - 50, cy - 110),
                "r_shoulder": (cx + 50, cy - 110),
                "l_hand": (cx - 90, cy - 60),
                "r_hand": (cx + 90, cy - 60),
                "l_foot": (cx - 35, cy + 200),
                "r_foot": (cx + 35, cy + 200),
            },
            "tpose": {
                "head": (cx, cy - 170),
                "neck": (cx, cy - 120),
                "hip": (cx, cy + 40),
                "l_shoulder": (cx - 50, cy - 110),
                "r_shoulder": (cx + 50, cy - 110),
                "l_hand": (cx - 180, cy - 110),
                "r_hand": (cx + 180, cy - 110),
                "l_foot": (cx - 35, cy + 200),
                "r_foot": (cx + 35, cy + 200),
            },
            "arms_up": {
                "head": (cx, cy - 170),
                "neck": (cx, cy - 120),
                "hip": (cx, cy + 40),
                "l_shoulder": (cx - 50, cy - 110),
                "r_shoulder": (cx + 50, cy - 110),
                "l_hand": (cx - 100, cy - 220),
                "r_hand": (cx + 100, cy - 220),
                "l_foot": (cx - 35, cy + 200),
                "r_foot": (cx + 35, cy + 200),
            },
        }

        if preset not in presets:
            preset = "standing"

        return self.create_pose_from_keypoints(width, height, presets[preset], stroke=stroke)

    def create_pose_from_keypoints(
        self,
        width: int,
        height: int,
        keypoints: Mapping[str, Tuple[int, int]],
        stroke: int = 10,
    ) -> Image.Image:
        img = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        def pt(name: str) -> Optional[Tuple[int, int]]:
            v = keypoints.get(name)
            if v is None:
                return None
            return int(v[0]), int(v[1])

        # Colors chosen to be high-contrast on black.
        COL_HEAD = (255, 0, 0)
        COL_BODY = (0, 160, 255)
        COL_ARMS = (50, 255, 50)
        COL_LEGS = (255, 140, 0)

        head = pt("head")
        neck = pt("neck")
        hip = pt("hip")
        l_shoulder = pt("l_shoulder")
        r_shoulder = pt("r_shoulder")
        l_hand = pt("l_hand")
        r_hand = pt("r_hand")
        l_foot = pt("l_foot")
        r_foot = pt("r_foot")

        if neck and hip:
            draw.line((neck[0], neck[1], hip[0], hip[1]), fill=COL_BODY, width=stroke)

        if neck and head:
            draw.line((neck[0], neck[1], head[0], head[1]), fill=COL_HEAD, width=stroke)
        if head:
            r = max(8, stroke * 2)
            draw.ellipse((head[0] - r, head[1] - r, head[0] + r, head[1] + r), fill=COL_HEAD)

        if neck and l_shoulder:
            draw.line((neck[0], neck[1], l_shoulder[0], l_shoulder[1]), fill=COL_ARMS, width=stroke)
        if neck and r_shoulder:
            draw.line((neck[0], neck[1], r_shoulder[0], r_shoulder[1]), fill=COL_ARMS, width=stroke)
        if l_shoulder and l_hand:
            draw.line((l_shoulder[0], l_shoulder[1], l_hand[0], l_hand[1]), fill=COL_ARMS, width=stroke)
        if r_shoulder and r_hand:
            draw.line((r_shoulder[0], r_shoulder[1], r_hand[0], r_hand[1]), fill=COL_ARMS, width=stroke)

        if hip and l_foot:
            draw.line((hip[0], hip[1], l_foot[0], l_foot[1]), fill=COL_LEGS, width=stroke)
        if hip and r_foot:
            draw.line((hip[0], hip[1], r_foot[0], r_foot[1]), fill=COL_LEGS, width=stroke)

        return img
