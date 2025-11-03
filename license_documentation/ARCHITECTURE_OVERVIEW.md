# Architecture Overview — DEX Shell

## High-level
DEX Shell is organized in layered modules:

1. **Core layer (Python)** — `core/` contains main runtime, command processor, plugin loader, and update hooks. It manages lifecycle and routes commands to plugins and system shell adapters.

2. **Interface layer (QML + OpenGL)** — `interface/` holds QML layouts, shaders, and a Python `layout_manager` that exposes a QML context. The UI is intentionally decoupled from the core logic via the `ctrl` object or IPC.

3. **Plugin layer** — `plugins/` contains multiple plugin categories (ai_plugin, audio_plugin, system_plugin). Plugins implement a small interface and register with `DexEngine`.

4. **Native modules (optional, C++)** — `sign_language/motion_tracker.cpp` and `commission_code/encrypt_layer.cpp` offer high-performance capture & crypto operations. Bindings are created via pybind11 or ctypes.

5. **Updates & Commission** — `updates/` handles manifest-driven patches, verification, and rollback. `commission_code/` offers license signing and AES helpers for encryption.

## Data Flow (Example: Gesture to Command)
- Motion tracker (C++ / MediaPipe) produces landmarks → `gesture_engine` consumes sequences → model predicts gesture id → `command_processor` maps gesture id to a command (using `gesture_reference/*.json`) → `DexEngine` executes command via plugin or system bridge.

## Security Considerations
- Signing patches and license files prevents tampering — verify signatures and checksums before apply.
- Backups are created prior to patch application to allow rollback.
- Private keys must be securely stored off-repo.

## Extensibility
- Add new plugins by implementing `PluginBase` and registering with `DexEngine`.
- UI extensions are QML components loaded by `layout_manager`.
- Native modules should expose clear, small API surfaces for Python bindings.