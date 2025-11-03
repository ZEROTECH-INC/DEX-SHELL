# System Specifications — DEX Shell (v0.9.4-alpha)

## Recommended (Development)
- OS: Ubuntu 20.04+ / Windows 10+ / macOS 12+
- CPU: 4-core or higher
- RAM: 8 GB minimum (16 GB recommended for ML training)
- GPU: Optional — NVIDIA with CUDA for TensorFlow training (if using GPU)
- Disk: 10 GB free for project + datasets

## Dependencies
- Python 3.9+
- PySide6 (Qt Quick)
- numpy, pandas
- OpenCV (python bindings) for camera capture
- TensorFlow (optional) for gesture model training
- CMake, a C++ compiler (g++, clang, or MSVC) for native modules
- OpenSSL dev libs for AES module

## Networking
- Updates can be hosted on an HTTPS server for manifest and patch artifacts.
- Local-only operation supported (example `updates/examples`)

## Privacy & Permissions
- Camera access consent must be obtained from users. Ensure local processing where possible and avoid uploading raw video without explicit consent.