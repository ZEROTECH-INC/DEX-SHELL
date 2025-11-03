# plugins/ — DEX Plugin Ecosystem

This folder contains modular plugins for DEX Shell. Each plugin is self-describing via a JSON config/manifest.

Structure:
- audio_plugin/      : Microphone audio detector (Python + C++ analyzer)
- ai_plugin/         : AI brain, gesture inference, and learning scripts
- system_plugin/     : Bridges to host shells (CMD, Bash, PowerShell)

How to add a plugin:
1. Create a folder under `plugins/<plugin_name>/`
2. Add `plugin_config.json` or `plugin_manifest.json` with metadata
3. Provide an `entry` or `entrypoints` key pointing to main script(s)
4. Ensure dependencies are listed and installed

Security:
- Avoid shipping secrets in plugin folders.
- Add sensitive output (keys, caches) to `.gitignore`.
- Use `secure_mode` in plugin manifest to enable stricter checks.

Example usage:
```bash
# run ai plugin (interactive)
python plugins/ai_plugin/ai_brain.py

# run audio plugin (requires sounddevice & numpy)
python plugins/audio_plugin/sound_detector.py

# run system plugin (cmd wrapper)
python plugins/system_plugin/cmd_wrapper.py
