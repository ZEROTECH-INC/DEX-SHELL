"""
DEX Installer Builder
---------------------
Packages the final executable and data assets into a distributable folder.
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

DIST_PATH = Path("dist")
BUILD_LOG = Path("build/logs/build.log")

def copy_assets():
    """Copy all essential directories for distribution."""
    required_dirs = ["core", "plugins", "interface", "os_layer", "launch_pack"]
    for d in required_dirs:
        if Path(d).exists():
            dest = DIST_PATH / d
            shutil.copytree(d, dest, dirs_exist_ok=True)
            print(f"[+] Copied {d} -> {dest}")

def generate_manifest():
    """Generate build manifest."""
    manifest = {
        "project": "DEX Shell",
        "version": "0.9.4-alpha",
        "build_time": datetime.now().isoformat(),
        "modules": ["core", "plugins", "interface", "os_layer", "launch_pack"],
        "author": "DEX Development Team"
    }
    (DIST_PATH / "build_manifest.json").write_text(json.dumps(manifest, indent=4))
    print("[+] Build manifest created.")

def compress_package():
    """Create compressed archive."""
    shutil.make_archive("DEX-Shell-Build", "zip", DIST_PATH)
    print("[+] DEX-Shell-Build.zip created.")

def main():
    print("Building installer package...")
    DIST_PATH.mkdir(parents=True, exist_ok=True)
    copy_assets()
    generate_manifest()
    compress_package()
    print("Installer build complete. Ready for distribution.")

if __name__ == "__main__":
    main()