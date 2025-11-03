#!/usr/bin/env python3
"""
updates/examples/build_patch_test.py
Builds a small test patch for DEX Shell update system.
Creates a zip archive with mock QML content and updates JSON manifests with size + SHA256.
"""

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATCH_ZIP = ROOT / "patch-ui-TEST.zip"
PATCH_JSON = ROOT / "patch-ui-TEST.json"
MANIFEST_JSON = ROOT / "update_manifest_test.json"


def make_mock_files(temp_dir: Path):
    """Create mock files to pack into the patch zip."""
    (temp_dir / "ai_assistant.qml").write_text(
        """// Mock QML patch - adds testing note
import QtQuick 2.15
Item {
    id: root
    Text {
        text: "DEX Shell UI Test Patch v0.9.5-test"
        color: "cyan"
        anchors.centerIn: parent
    }
}
"""
    )


def build_zip():
    import tempfile, shutil

    tmp = Path(tempfile.mkdtemp(prefix="dex_patch_build_"))
    make_mock_files(tmp)

    with zipfile.ZipFile(PATCH_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for file in tmp.rglob("*"):
            z.write(file, arcname=file.relative_to(tmp))

    shutil.rmtree(tmp)
    print(f"[+] Created patch: {PATCH_ZIP}")


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def update_json_files():
    sha = compute_sha256(PATCH_ZIP)
    size = PATCH_ZIP.stat().st_size

    for json_path in [PATCH_JSON, MANIFEST_JSON]:
        data = json.loads(json_path.read_text())
        if "sha256" in data:
            data["sha256"] = sha
            data["size_bytes"] = size
        elif "releases" in data:
            for rel in data["releases"]:
                for patch in rel["patches"]:
                    patch["sha256"] = sha
                    patch["size_bytes"] = size
        json_path.write_text(json.dumps(data, indent=2))
        print(f"[+] Updated {json_path.name} (SHA256 + size)")


if __name__ == "__main__":
    build_zip()
    update_json_files()
    print("[✓] Patch test build complete!")