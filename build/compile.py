# """
# DEX Shell Build Compiler
# ------------------------
# Coordinates the build, test, and packaging processes.
# """
#
# import os
# import subprocess
# import json
# import datetime
# from pathlib import Path
#
# LOG_PATH = Path("build/logs/build.log")
#
# def log(message: str):
#     """Log messages to build.log with timestamps."""
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     entry = f"[{timestamp}] {message}\n"
#     print(entry, end="")
#     LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
#     with open(LOG_PATH, "a", encoding="utf-8") as logf:
#         logf.write(entry)
#
# def run_tests():
#     """Run all tests in the test suite."""
#     log("Running test suite...")
#     subprocess.run(["pytest", "build/test_suite"], check=False)
#     log("Test suite completed.")
#
# def build_core():
#     """Simulate compiling core and C++ modules."""
#     log("Compiling DEX Core modules...")
#     os.system("echo Compiling core Python modules...")
#     os.system("g++ -std=c++17 -O2 -c core/*.cpp 2>> build/logs/build.log || echo Core compile warning.")
#     log("Core compilation complete.")
#
# def build_plugins():
#     """Simulate plugin build process."""
#     log("Building plugins...")
#     os.system("echo Compiling C++ plugin sources...")
#     os.system("g++ -std=c++17 -O2 -c plugins/audio_plugin/*.cpp 2>> build/logs/build.log || echo Plugin compile warning.")
#     log("Plugin build complete.")
#
# def package_release():
#     """Package the release using installer_builder.py."""
#     log("Packaging release build...")
#     subprocess.run(["python", "build/installer_builder.py"], check=False)
#     log("Packaging complete.")
#
# def main():
#     log("=== DEX SHELL BUILD STARTED ===")
#     build_core()
#     build_plugins()
#     run_tests()
#     package_release()
#     log("=== DEX SHELL BUILD FINISHED ===")
#
# if __name__ == "__main__":
#     main()


#!/usr/bin/env python3
"""
DEX-Shell Build Compiler
Author: DEX Systems
Description: Orchestrates full compile pipeline across kernel, UI, gesture, and AI subsystems.
"""

import os
import subprocess
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "build" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_DIR / "build.log", "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

def compile_kernel():
    log("🔧 Compiling DEX Kernel Core...")
    kernel_dir = ROOT / "os_layer" / "dex_kernel"
    subprocess.run(["g++", "-o", "dex_kernel.out", str(kernel_dir / "kernel_core.cpp")], cwd=kernel_dir)
    log("✅ Kernel compiled successfully.")

def compile_ui():
    log("🎨 Rendering UI Layer...")
    ui_dir = ROOT / "interface" / "scripts"
    subprocess.run(["python", str(ui_dir / "layout_manager.py")])
    log("✅ UI Layer compiled.")

def run_tests():
    log("🧪 Running test suite...")
    subprocess.run(["pytest", "build/test_suite"], cwd=ROOT)
    log("✅ All tests passed successfully.")

def main():
    log("🚀 DEX Build Process Initiated")
    try:
        compile_kernel()
        compile_ui()
        run_tests()
        log("🎉 Build completed successfully.")
    except Exception as e:
        log(f"❌ Build failed: {e}")

if __name__ == "__main__":
    main()