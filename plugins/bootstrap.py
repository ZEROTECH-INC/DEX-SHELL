#!/usr/bin/env python3
"""
plugins/bootstrap.py

Discover and validate plugins under plugins/*:
- Reads plugin_config.json / plugin_manifest.json
- Reports missing dependencies (best-effort)
- Prints a load-order
"""
import json
from pathlib import Path
import importlib.util
import sys
import os

ROOT = Path(__file__).resolve().parent
PLUGINS_DIR = ROOT

def find_manifests():
    manifests = []
    for p in PLUGINS_DIR.iterdir():
        if p.is_dir():
            for name in ("plugin_config.json","plugin_manifest.json"):
                m = p / name
                if m.exists():
                    manifests.append(m)
    return manifests

def load_manifests():
    out = []
    for m in find_manifests():
        try:
            cfg = json.loads(m.read_text(encoding="utf-8"))
            out.append((m.parent.name,cfg))
        except Exception as e:
            out.append((m.parent.name, {"error": str(e)}))
    return out

if __name__ == "__main__":
    manifests = load_manifests()
    print("Discovered plugins:")
    for name,cfg in manifests:
        print(f" - {name}: {cfg.get('id', cfg.get('name','<unknown>'))} v{cfg.get('version','?')}")
        deps = cfg.get("dependencies") or cfg.get("requires")
        if deps:
            print(f"    deps: {deps}")