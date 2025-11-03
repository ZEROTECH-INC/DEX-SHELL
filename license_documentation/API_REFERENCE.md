# API Reference — DEX Shell (v0.9.4-alpha)

This document lists the public-facing modules, QML interfaces, and IPC hooks used by DEX Shell.

## Python Modules (public functions/classes)

### `core/dex_engine.py`
- `DexEngine` (class)
  - `start()`
  - `stop()`
  - `register_plugin(plugin: Plugin)`
  - `execute_command(cmd: str) -> CommandResult`

### `core/command_processor.py`
- `process_command(cmd: str) -> Dict` — parses and routes commands (system vs plugin vs AI)

### `sign_language/gesture_engine.py`
- `load_csv_sequences(path, seq_len)` — load dataset
- `build_model(input_shape, n_classes)` — construct Keras model
- `train(csv_path, epochs, ...)` — train and save
- `GestureEngine(model_path, label_json)` — class
  - `predict_from_sequence(seq)`
  - `capture_and_predict(cam_index, seq_len)`

### `updates/update_manager.py`
- `UpdateManager(manifest_source, repo_root=None)`
  - `load_manifest()`
  - `list_available_patches()`
  - `apply_patch(patch_dict)`
  - `rollback(backup_id)`

### `commission_code/key_generator.py`
- `gen_keys(outdir, passphrase)`
- `sign_payload(private_key, payload_bytes)`
- `verify_signature(public_key, payload_bytes, signature)`

## QML Exposed Context Objects
- `ctrl` — application controller exposed by `interface/scripts/layout_manager.py`
  - Properties: `consoleText`, `plugins`, `cpuUsage`, `memUsage`, `aiConversation`
  - Methods/Slots: `handleCommand(str)`, `sendMessage(str)`
- `theme` — theme JSON mapped into QML (keys: background, panel, text, accent, font)

## Filesystem / Update Hooks
- Update manifests live at `updates/update_manifest.json`.
- Patch artifacts are expected to be zip archives containing relative paths.

## Network / IPC
DEX does not ship a single IPC standard; recommended integration points:
- UNIX domain socket or named pipe for local `core` ↔ `UI` messaging.
- HTTP REST endpoint for plugin status and telemetry (if enabled) — secure with local-only binding.

## Example: Calling the gesture engine from Python
```python
from sign_language.gesture_engine import GestureEngine
ge = GestureEngine('gesture_model.h5','label_encoder.json')
label, prob = ge.capture_and_predict(0)
print(label, prob)