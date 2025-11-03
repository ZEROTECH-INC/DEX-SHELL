import json
import os
import subprocess
from pathlib import Path

REPO_MANIFEST = Path(__file__).parent / "repo_manifest.json"

def load_manifest():
    return json.loads(REPO_MANIFEST.read_text())

def install_package(pkg_name):
    data = load_manifest()
    if pkg_name not in data["available_packages"]:
        print(f"[ERROR] Package {pkg_name} not found in repo.")
        return
    url = data["available_packages"][pkg_name]["url"]
    print(f"[DEX-PKG] Installing {pkg_name} from {url} ...")
    # simulate download
    subprocess.run(["echo", f"Downloading {pkg_name}..."], shell=True)
    print(f"[DEX-PKG] {pkg_name} installed successfully.")

def list_packages():
    data = load_manifest()
    print("[DEX-PKG] Available Packages:")
    for name, info in data["available_packages"].items():
        print(f"  - {name} ({info['version']}) → {info['url']}")

if __name__ == "__main__":
    list_packages()