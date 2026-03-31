import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ProjectPaths:
    root: str
    ref_dir: str
    renders_dir: str


def resolve_project_paths(project_root: str) -> ProjectPaths:
    root = os.path.abspath(project_root)
    return ProjectPaths(
        root=root,
        ref_dir=os.path.join(root, "ref"),
        renders_dir=os.path.join(root, "renders"),
    )


def ensure_project_dirs(project_root: str) -> ProjectPaths:
    paths = resolve_project_paths(project_root)
    os.makedirs(paths.root, exist_ok=True)
    os.makedirs(paths.ref_dir, exist_ok=True)
    os.makedirs(paths.renders_dir, exist_ok=True)
    return paths


def validate_project(project_root: str) -> Tuple[bool, List[str]]:
    """
    Lightweight structural validation for an AnchorFrame project directory.
    Returns (ok, messages). Messages are human-readable.
    """
    paths = resolve_project_paths(project_root)
    messages: List[str] = []

    if not os.path.isdir(paths.root):
        return False, [f"Project root does not exist: {paths.root}"]

    for d in (paths.ref_dir, paths.renders_dir):
        if not os.path.isdir(d):
            messages.append(f"Missing directory: {d}")

    ok = len(messages) == 0
    if ok:
        messages.append("Project structure looks good.")
    return ok, messages


def env_status(required: Optional[List[str]] = None) -> Dict[str, str]:
    keys = required or ["COMFY_UI_URL", "OUTPUT_DIR", "ELEVEN_LABS_API_KEY"]
    out: Dict[str, str] = {}
    for k in keys:
        v = os.getenv(k)
        if v is None or v == "":
            out[k] = "(missing)"
        elif "KEY" in k or "TOKEN" in k or "SECRET" in k:
            out[k] = "(set)"
        else:
            out[k] = v
    return out

