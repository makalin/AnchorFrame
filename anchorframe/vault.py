import json
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Optional


VAULT_DIRNAME = ".anchorframe"
VAULT_FILENAME = "vault.json"
VAULT_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class VaultPaths:
    root: str
    vault_dir: str
    vault_file: str


def resolve_vault_paths(project_root: str) -> VaultPaths:
    root = os.path.abspath(project_root)
    vault_dir = os.path.join(root, VAULT_DIRNAME)
    vault_file = os.path.join(vault_dir, VAULT_FILENAME)
    return VaultPaths(root=root, vault_dir=vault_dir, vault_file=vault_file)


def _empty_vault() -> Dict:
    return {
        "schema_version": VAULT_SCHEMA_VERSION,
        "created_at": int(time.time()),
        "assets": {},  # name -> record
    }


def load_vault(project_root: str) -> Dict:
    paths = resolve_vault_paths(project_root)
    if not os.path.exists(paths.vault_file):
        return _empty_vault()
    with open(paths.vault_file, "r") as f:
        data = json.load(f)
    if not isinstance(data, dict) or data.get("schema_version") != VAULT_SCHEMA_VERSION:
        # Minimal safety: don't try to auto-migrate yet.
        raise ValueError(f"Unsupported vault schema in {paths.vault_file}")
    if "assets" not in data or not isinstance(data["assets"], dict):
        data["assets"] = {}
    return data


def save_vault(project_root: str, vault: Dict) -> VaultPaths:
    paths = resolve_vault_paths(project_root)
    os.makedirs(paths.vault_dir, exist_ok=True)
    with open(paths.vault_file, "w") as f:
        json.dump(vault, f, indent=2)
    return paths


def list_assets(project_root: str) -> List[Dict]:
    vault = load_vault(project_root)
    assets = []
    for name, rec in vault.get("assets", {}).items():
        assets.append({"name": name, **rec})
    assets.sort(key=lambda a: a["name"].lower())
    return assets


def get_asset(project_root: str, name: str) -> Optional[Dict]:
    vault = load_vault(project_root)
    rec = vault.get("assets", {}).get(name)
    if rec is None:
        return None
    return {"name": name, **rec}


def add_asset(project_root: str, name: str, image_path: str, type: str = "person") -> Dict:
    vault = load_vault(project_root)
    now = int(time.time())
    record = {
        "type": type,
        "image_path": image_path,
        "added_at": now,
        "exists": os.path.exists(os.path.join(os.path.abspath(project_root), image_path))
        if not os.path.isabs(image_path)
        else os.path.exists(image_path),
        "embedding": None,
    }
    vault.setdefault("assets", {})[name] = record
    save_vault(project_root, vault)
    return {"name": name, **record}


def remove_asset(project_root: str, name: str) -> bool:
    vault = load_vault(project_root)
    assets = vault.get("assets", {})
    if name not in assets:
        return False
    del assets[name]
    save_vault(project_root, vault)
    return True

