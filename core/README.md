# core/ — DEX Core Components

This folder contains the primary runtime and engine stubs for DEX.

Files:
- `main.py` - Orchestrator / REPL and API server
- `dex_engine.cpp` - Optional native engine (C++) for high-performance tasks
- `dex_interface.qml` - Minimal QML preview for the UI layer
- `dex_runtime.cs` - C# runtime skeleton for Windows-specific or high-speed services
- `dex_main.js` - Node helper for serving static previews or running dev tools
- `config.json` - Default core configuration

## Getting Started

Python:
```bash
# run the core orchestrator
python core/main.py
````

C++ (optional):

```bash
# compile (Linux/Mac)
g++ core/dex_engine.cpp -std=c++17 -O2 -o core/dex_engine
# run the native engine (optional)
core/dex_engine
```

C# (optional):

```bash
# create a .NET project (if not already)
cd core
dotnet new console -n DexRuntime
# replace Program.cs with dex_runtime.cs content or add it to project and build
dotnet run --project DexRuntime
```

Node helper:

```bash
# run the dev static server
node core/dex_main.js
```

Notes:

* These stubs are intentionally minimal to make rapid iteration easy. Replace parts with your own implementations as the project grows.
* The QML file is a preview stub; your real UI will live in the `ui/` directory and import core APIs.

```


### Quick next steps & tips
- Save each block into the files shown above under `core/`.
- Make `main.py` executable and ensure Python 3.10+ is installed.
- If you want to enable `engine_native` in `config.json`, compile the C++ file and set the flag to `true`.
- For development convenience, add these dev entries to `pyproject.toml` or a Makefile to build / run components quickly.

