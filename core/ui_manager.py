# core/ui_manager.py
import os
from flask import Flask, send_file, jsonify
from flask import Flask, render_template

app = Flask(__name__)

# Path to main interface file
UI_PATH = os.path.join(os.path.dirname(__file__), "../interface/layout/main_interface.ui")

@app.route("/")
def serve_ui():
    if os.path.exists(UI_PATH):
        return send_file(UI_PATH)
    return jsonify({"error": "UI file not found", "path": UI_PATH}), 404

@app.route("/status")
def status():
    return jsonify({"status": "DEX UI Manager active", "ui_path": UI_PATH})

def run_ui_server():
    print("🚀 Launching DEX UI Server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)

@app.route('/favicon.ico')
def favicon():
    icon_path = os.path.join(os.path.dirname(__file__), '../interface/assets/icons/dex_icon.ico')
    if os.path.exists(icon_path):
        return send_file(icon_path)
    return '', 204

app = Flask(__name__, template_folder="../interface/layout", static_folder="../interface/assets")

@app.route('/')
def index():
    return render_template('main_interface.html')

if __name__ == "__main__":
    app.run(debug=True)

#
# if __name__ == "__main__":
#     run_ui_server()

