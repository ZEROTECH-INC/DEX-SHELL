#!/usr/bin/env bash
# plugins/system_plugin/bash_bridge.sh
# Simple interactive bridge for Bash-like shells (POSIX)
echo "[dex.system.bash] Interactive shell. Type 'exit' to quit."
while true; do
  read -p "bash> " cmd
  if [[ "$cmd" == "exit" ]]; then break; fi
  eval "$cmd"
done