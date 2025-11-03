#!/usr/bin/env python3
# core/main.py
"""
DEX Core Launcher
- Loads config.json
- Starts optional native engine (dex_engine native module)
- Provides CLI for run/debug and a small local HTTP API for UI integration
"""

import json
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"

DEFAULT_PORT = 8765

def load_config():
    if not CONFIG_PATH.exists():
        print("Config missing, using defaults.")
        return {"name":"DEX Shell", "version":"0.1.0", "port": DEFAULT_PORT, "engine_native": False}
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def _json(self, obj, status=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/status":
            self._json({"status":"ok","service":"dex_core"})
        elif self.path == "/version":
            self._json({"version": cfg.get("version")})
        else:
            self.send_response(404)
            self.end_headers()

def run_api_server(port):
    server = HTTPServer(("127.0.0.1", port), SimpleAPIHandler)
    print(f"[core] API server listening on http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

def start_native_engine():
    """
    Attempt to start compiled native engine binary (if present).
    Expects 'dex_engine' binary in same folder (or dex_engine.dll / dex_engine.so)
    """
    candidates = ["dex_engine", "dex_engine.exe", "dex_engine.so", "dex_engine.dylib"]
    for name in candidates:
        path = ROOT / name
        if path.exists():
            print(f"[core] Starting native engine: {path}")
            # start as background process
            proc = subprocess.Popen([str(path)])
            return proc
    print("[core] Native engine not found, running pure-python fallback.")
    return None

def repl_loop():
    print("DEX Core REPL. Type 'help' for commands. Ctrl-C to quit.")
    while True:
        try:
            cmd = input("dex> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting REPL.")
            break
        if not cmd:
            continue
        if cmd in ("exit","quit"):
            break
        elif cmd == "help":
            print("Commands: help, status, version, spawn, stop, exit")
        elif cmd == "status":
            print("Service: dex_core, status: running")
        elif cmd == "version":
            print(f"DEX Core version: {cfg.get('version')}")
        elif cmd == "spawn":
            print("Spawn engine (if available).")
            start_native_engine()
        else:
            print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    cfg = load_config()
    print(f"[core] Starting {cfg.get('name')} v{cfg.get('version')}")
    # start API server in background thread
    api_port = cfg.get("port", DEFAULT_PORT)
    api_thread = threading.Thread(target=run_api_server, args=(api_port,), daemon=True)
    api_thread.start()

    native_proc = None
    if cfg.get("engine_native", False):
        native_proc = start_native_engine()

    try:
        repl_loop()
    finally:
        if native_proc:
            try:
                native_proc.terminate()
            except Exception:
                pass
        print("[core] Shutdown complete.")

from ui_manager import run_ui_server

if __name__ == "__main__":
    print("🧠 Initializing DEX Engine Core...")
    run_ui_server()
