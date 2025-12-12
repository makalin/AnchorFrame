from anchorframe import Director, Asset, Scene
from anchorframe.logic import PoseProxy, LLMDirector
from anchorframe.providers import LocalComfyProvider
from anchorframe.utils.logger import configure_logger
import os

def main():
    # 0. Setup Logger
    logger = configure_logger()
    
    # 1. Initialize Components
    logger.info("=== AnchorFrame Movie Studio ===")
    
    # Use the refactored Provider
    provider = LocalComfyProvider("http://127.0.0.1:8188")
    director = Director(project="The_Last_Droid", provider=provider)

    # 2. The Script (LLM Director Demo)
    script = """
    [INT_SPACESHIP_BAY]
    DROID: "System check complete." (Action: checking console)
    DROID: "Engines are offline." (Action: turning head)
    """
    
    # 3. Parse Script
    llm = LLMDirector() # Mock
    parsed_shots = llm.convert_script(script)
    logger.info(f"LLM parsed {len(parsed_shots)} shots from script.")
    
    # 4. Prepare Assets
    if not os.path.exists("./ref"): os.makedirs("./ref")
    
    proxy = PoseProxy()
    droid_pose = proxy.create_pose()
    droid_pose.save("./ref/droid_pose.png")
    
    droid_asset = Asset("Droid_01", "./ref/droid_pose.png", "character")
    bg_asset = Scene("./ref/spaceship.png", lock_camera=True)
    
    # 5. Direct the Movie
    for shot in parsed_shots:
        # Map scene_id to actual Scene object (simplified)
        director.shoot(
            assets=[droid_asset],
            scene=bg_asset,
            prompt=shot['prompt'], # "DROID checking console..."
            audio_text=shot['dialogue'], # "System check complete."
            frames=48
        )

    # 6. Action
    director.action()

if __name__ == "__main__":
    main()
