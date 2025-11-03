import subprocess
import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

def start_kernel():
    print("[DEX-OS] Launching kernel simulation...")
    subprocess.run(["./dex_kernel/kernel_core"], check=False)

def start_desktop():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(QUrl("desktop_environment.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    print("[DEX-OS] Desktop environment loaded.")
    sys.exit(app.exec())

if __name__ == "__main__":
    start_kernel()
    start_desktop()