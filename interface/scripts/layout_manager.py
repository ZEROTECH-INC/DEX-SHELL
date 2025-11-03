"""
layout_manager.py

PySide6 app that loads the QML layouts and exposes a simple controller object
(`ctrl`) to the QML context. This controller provides functions and properties
used by the QML UIs (console text, plugins list, system stats, gestures, etc.).

Run: python layout_manager.py
Requires: PySide6
"""
import sys
import json
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal, Property, QUrl, Qt
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QGuiApplication, QFontDatabase

HERE = Path(__file__).resolve().parent.parent
ASSETS = HERE / 'assets'
THEMES_DIR = ASSETS / 'themes'
FONTS_DIR = ASSETS / 'fonts'
LAYOUT_DIR = HERE / 'layout'


class Controller(QObject):
    consoleTextChanged = Signal()

    def __init__(self):
        super().__init__()
        self._console_text = "DEX Shell initialized..."
        self.plugins = ['ai_plugin', 'audio_plugin', 'system_plugin']
        self.gestureMap = [
            {'icon': 'icons/dex_icon.svg', 'name': 'Wave', 'desc': 'Open assistant'},
            {'icon': 'icons/dex_icon.svg', 'name': 'Fist', 'desc': 'Lock input'}
        ]
        self.cpuUsage = 12.3
        self.memUsage = 41.7
        self.aiModel = 'dex-ghost-0.1'
        self.aiStatus = 'idle'
        self.aiConversation = [ {'role': 'assistant', 'text': 'Hello. I am DEX.'} ]

    @Property(str, notify=consoleTextChanged)
    def consoleText(self):
        return self._console_text

    @Slot(str)
    def handleCommand(self, cmd: str):
        if not cmd:
            return
        self._console_text += f"> {cmd}"
        self.consoleTextChanged.emit()
        # basic mock: echo + pseudo-processing
        if cmd.lower().startswith('echo '):
            self._console_text += cmd[5:] + ""
        elif cmd.lower() == 'status':
            self._console_text += f"CPU: {self.cpuUsage}%, MEM: {self.memUsage}%"
        else:
            self._console_text += "[dex] Unknown command"
        self.consoleTextChanged.emit()

    @Slot(str)
    def sendMessage(self, text: str):
        if not text:
            return
        self.aiConversation.append({'role': 'user', 'text': text})
        # mock assistant reply
        self.aiConversation.append({'role': 'assistant', 'text': 'Processing... (mock)'} )


def load_theme(theme_name: str = 'dark_mode.json'):
    path = THEMES_DIR / theme_name
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def register_fonts():
    # load fonts from assets/fonts
    if FONTS_DIR.exists():
        for f in FONTS_DIR.iterdir():
            if f.suffix.lower() in ('.ttf', '.otf'):
                QFontDatabase.addApplicationFont(str(f))


def main():
    app = QGuiApplication(sys.argv)
    register_fonts()

    engine = QQmlApplicationEngine()

    ctrl = Controller()

    theme = load_theme('dark_mode.json')

    # expose objects to QML
    engine.rootContext().setContextProperty('ctrl', ctrl)
    engine.rootContext().setContextProperty('theme', theme)

    # load main dashboard by default
    main_qml = LAYOUT_DIR / 'system_dashboard.qml'
    engine.load(QUrl.fromLocalFile(str(main_qml)))

    if not engine.rootObjects():
        print('Failed to load QML. Check paths and Qt installation.')
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()