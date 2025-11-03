#!/usr/bin/env python3
"""
plugins/system_plugin/cmd_wrapper.py

Execute host OS shell commands securely; returns dict with output/status.
WARNING: Be careful with arbitrary execution - integrate sanitization.
"""
import subprocess, shlex, platform, json

PLUGIN = "dex.system.cmd"

def run_command(command: str, shell=False, timeout=30):
    if isinstance(command, (list, tuple)):
        cmd = command
    else:
        # naive sanitization: disallow null bytes
        if "\x00" in command:
            return {"status":"error","error":"invalid input"}
        # split for safety if not using shell
        if not shell:
            cmd = shlex.split(command)
        else:
            cmd = command
    try:
        out = subprocess.check_output(cmd, shell=shell, stderr=subprocess.STDOUT, timeout=timeout)
        return {"status":"ok","output": out.decode(errors="ignore")}
    except subprocess.CalledProcessError as e:
        return {"status":"error","output": e.output.decode(errors="ignore"), "code": e.returncode}
    except Exception as e:
        return {"status":"error","error": str(e)}

if __name__ == "__main__":
    print("[dex.system.cmd] Ready. Type 'exit' to quit.")
    try:
        while True:
            c = input("cmd> ")
            if c.strip().lower() in ("exit","quit"): break
            print(json.dumps(run_command(c), indent=2))
    except KeyboardInterrupt:
        pass
