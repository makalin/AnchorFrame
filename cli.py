import click
import os
import json
from anchorframe import Director, Asset, Scene
from anchorframe.logic import PoseProxy
from anchorframe.utils.logger import configure_logger
from anchorframe.utils import ensure_project_dirs, validate_project, env_status
from anchorframe.graph_builder import GraphBuilder
from anchorframe.providers import LocalComfyProvider
from anchorframe.post.video_assembler import VideoAssembler
from anchorframe.vault import add_asset, get_asset, list_assets, remove_asset, load_vault, save_vault

@click.group()
def cli():
    """AnchorFrame CLI"""
    pass

@cli.command()
@click.argument('project_name')
def init(project_name):
    """Initialize a new project structure."""
    paths = ensure_project_dirs(project_name)
    
    # Create a simple script inside
    script_path = os.path.join(project_name, "script.py")
    with open(script_path, "w") as f:
        f.write("# AnchorFrame Script\n")
        f.write("from anchorframe import Director, Asset, Scene\n\n")
        f.write("# director = Director('MyMovie')\n")
    
    click.echo(f"Initialized project '{project_name}'")
    click.echo(f"- ref: {paths.ref_dir}")
    click.echo(f"- renders: {paths.renders_dir}")


@cli.command()
@click.option("--comfy-url", default=None, help="Override COMFY_UI_URL for this check")
def status(comfy_url):
    """Show env status and backend reachability."""
    logger = configure_logger()
    if comfy_url:
        os.environ["COMFY_UI_URL"] = comfy_url
    comfy = os.getenv("COMFY_UI_URL", "http://127.0.0.1:8188")
    reachable = LocalComfyProvider(comfy).is_reachable()

    click.echo("Environment:")
    for k, v in env_status().items():
        click.echo(f"- {k}={v}")
    click.echo("")
    click.echo(f"ComfyUI: {comfy}")
    click.echo(f"Reachable: {reachable}")
    if not reachable:
        logger.warning("Backend not reachable. Start ComfyUI with --listen, or set COMFY_UI_URL.")


@cli.command()
@click.argument("project_root", default=".")
def validate(project_root):
    """Validate an AnchorFrame project directory."""
    ok, messages = validate_project(project_root)
    for m in messages:
        click.echo(m)
    raise SystemExit(0 if ok else 2)


@cli.command()
@click.option("--preset", type=click.Choice(["standing", "tpose", "arms_up"]), default="standing")
@click.option("--width", default=512, type=int)
@click.option("--height", default=512, type=int)
@click.option("--stroke", default=10, type=int)
@click.option("--out", "out_path", default="renders/pose.png", help="Output PNG path")
def pose(preset, width, height, stroke, out_path):
    """Generate a PoseProxy PNG."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    proxy = PoseProxy()
    img = proxy.create_pose(width=width, height=height, preset=preset, stroke=stroke)
    img.save(out_path)
    click.echo(f"Saved pose: {out_path}")


@cli.group()
def vault():
    """Manage project asset vault (.anchorframe/vault.json)."""
    pass


@vault.command("init")
@click.argument("project_root", default=".")
def vault_init(project_root):
    """Create an empty vault file if missing."""
    v = load_vault(project_root)
    paths = save_vault(project_root, v)
    click.echo(f"Vault ready: {paths.vault_file}")


@vault.command("add")
@click.option("--project", "project_root", default=".", help="Project root directory")
@click.option("--name", required=True, help="Asset name (unique key)")
@click.option("--image", "image_path", required=True, help="Image path (relative to project or absolute)")
@click.option("--type", "asset_type", default="person", help="Asset type (person/prop/pose/...)")
def vault_add(project_root, name, image_path, asset_type):
    """Add or update an asset record."""
    rec = add_asset(project_root, name=name, image_path=image_path, type=asset_type)
    click.echo(json.dumps(rec, indent=2))


@vault.command("list")
@click.argument("project_root", default=".")
def vault_list(project_root):
    """List assets in the vault."""
    assets = list_assets(project_root)
    if not assets:
        click.echo("No assets in vault.")
        return
    for a in assets:
        exists = "ok" if a.get("exists") else "missing"
        click.echo(f"- {a['name']} ({a.get('type','?')}) [{exists}] -> {a.get('image_path')}")


@vault.command("show")
@click.option("--project", "project_root", default=".", help="Project root directory")
@click.argument("name")
def vault_show(project_root, name):
    """Show a single asset record as JSON."""
    rec = get_asset(project_root, name)
    if rec is None:
        raise SystemExit(2)
    click.echo(json.dumps(rec, indent=2))


@vault.command("rm")
@click.option("--project", "project_root", default=".", help="Project root directory")
@click.argument("name")
def vault_rm(project_root, name):
    """Remove an asset record."""
    ok = remove_asset(project_root, name)
    raise SystemExit(0 if ok else 2)


@cli.command()
@click.option("--dir", "source_dir", required=True, help="Directory containing frames")
@click.option("--out", "output_path", required=True, help="Output .mp4 path")
@click.option("--fps", default=24, type=int, help="Frames per second")
@click.option("--pattern", default="*.png", help="Glob pattern for frames (default: *.png)")
def assemble(source_dir, output_path, fps, pattern):
    """Assemble a video from rendered frames."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    VideoAssembler(fps=fps).make_video(source_dir=source_dir, output_path=output_path, file_pattern=pattern)


@cli.command()
@click.option("--prompt", default="A cinematic portrait, ultra-detailed")
@click.option("--seed", default=0, type=int)
@click.option("--frames", default=24, type=int)
@click.option("--out", "out_path", default="renders/workflow.json", help="Output workflow JSON path")
def graph(prompt, seed, frames, out_path):
    """Build and save a ComfyUI workflow JSON (dry-run)."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    builder = GraphBuilder()
    workflow = builder.build_workflow({"prompt": prompt, "seed": seed, "frames": frames})
    with open(out_path, "w") as f:
        json.dump(workflow, f, indent=2)
    click.echo(f"Saved workflow: {out_path}")

@cli.command()
@click.option('--dry-run', is_flag=True, help='Run without connecting to ComfyUI')
def demo(dry_run):
    """Runs a demonstration with PoseProxy."""
    logger = configure_logger()
    logger.info("Starting Demo Mode...")
    
    # 1. Create a dummy pose
    logger.info("Generating Pose Proxy...")
    proxy = PoseProxy()
    pose_img = proxy.create_pose(width=512, height=512, preset="standing")
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
