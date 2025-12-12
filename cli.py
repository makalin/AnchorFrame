import click
import os
from anchorframe import Director, Asset, Scene
from anchorframe.logic import PoseProxy
from anchorframe.utils.logger import configure_logger

@click.group()
def cli():
    """AnchorFrame CLI"""
    pass

@cli.command()
@click.argument('project_name')
def init(project_name):
    """Initialize a new project structure."""
    os.makedirs(project_name, exist_ok=True)
    os.makedirs(os.path.join(project_name, "ref"), exist_ok=True)
    os.makedirs(os.path.join(project_name, "renders"), exist_ok=True)
    
    # Create a simple script inside
    script_path = os.path.join(project_name, "script.py")
    with open(script_path, "w") as f:
        f.write("# AnchorFrame Script\n")
        f.write("from anchorframe import Director, Asset, Scene\n\n")
        f.write("# director = Director('MyMovie')\n")
    
    click.echo(f"Initialized project '{project_name}'")

@cli.command()
@click.option('--dry-run', is_flag=True, help='Run without connecting to ComfyUI')
def demo(dry_run):
    """Runs a demonstration with PoseProxy."""
    logger = configure_logger()
    logger.info("Starting Demo Mode...")
    
    # 1. Create a dummy pose
    logger.info("Generating Pose Proxy...")
    proxy = PoseProxy()
    pose_img = proxy.create_pose(width=512, height=512)
    os.makedirs("renders", exist_ok=True)
    pose_img.save("renders/demo_pose.png")
    logger.info("Saved 'renders/demo_pose.png'")
    
    # 2. Run Director
    director = Director(project="Demo_Project")
    
    hero = Asset(name="Hero", image_path="renders/demo_pose.png", type="pose")
    bg = Scene(image_path="ref/bridge.png", lock_camera=True)
    
    director.shoot([hero], bg, "A hero standing in a sci-fi corridor", frames=24)
    director.action()

if __name__ == '__main__':
    cli()
