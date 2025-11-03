# Developer Guide — DEX Shell

This guide helps new contributors set up a development environment, follow coding standards, and run tests.

## Setup
1. Clone the repository:
```bash
git clone git@example.com:dex-shell/dex-shell.git
cd dex-shell
````

2. Create a virtual environment and install Python deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Install optional native dependencies (OpenCV, OpenSSL dev libs, CMake) for building C++ modules.

## Coding Guidelines

* Python: follow PEP8. Use type annotations where reasonable.
* QML: keep UI logic minimal; prefer exposing functions via `ctrl`.
* C++: use modern C++ (>= C++11). Keep ABI stable; export small functions for bindings.
* Commit messages: reference ticket/issue IDs, include short summary and rationale.

## Branching & Releases

* `main` for stable releases.
* `develop` for ongoing integration.
* Feature branches: `feature/xxx` or `hotfix/xxx`.

## Testing

* Unit tests: place under `tests/` and run via pytest.
* ML tests: include small synthetic dataset checks for model shape and accuracy thresholds.

## Local Dev Workflows

* Start UI only:

```bash
python interface/scripts/layout_manager.py
```

* Train (fast smoke test):

```bash
python sign_language/gesture_engine.py --train sign_language/training_dataset/gestures_sample_1000.csv --epochs 1
```

* Build native modules:

```bash
cd sign_language && mkdir build && cd build && cmake .. && cmake --build .
```

## Code Review Checklist

* Tests updated/added
* No hardcoded secrets
* Documentation updated (`docs/`)
* Backwards-compatible API changes documented in `CHANGELOG.md`