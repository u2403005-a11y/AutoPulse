import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

ROOT = Path(__file__).parent
FRONTEND_DIR = ROOT / "frontend"
MODEL_DIR = ROOT / "model"
DB_PATH = ROOT / "database" / "predictions.db"


def pip_install_requirements():
    req = ROOT / "requirements.txt"
    if not req.exists():
        print("requirements.txt missing, skipping pip install")
        return
    print("Installing Python packages from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req)])


def npm_install_and_build():
    # install and build frontend
    if not (FRONTEND_DIR / "package.json").exists():
        print("No frontend/package.json found, skipping npm tasks")
        return
    print("Running npm install (this may take a while)...")
    try:
        subprocess.check_call(["npm", "install"], cwd=str(FRONTEND_DIR))
    except Exception as e:
        print("npm install failed:", e)
        return
    print("Building frontend (Vite)...")
    try:
        subprocess.check_call(["npm", "run", "build"], cwd=str(FRONTEND_DIR))
    except Exception as e:
        print("npm build failed:", e)


def ensure_model_trained():
    MODEL_DIR.mkdir(exist_ok=True)
    model_file = MODEL_DIR / "model.joblib"
    if model_file.exists():
        print("Model already trained.")
        return
    print("Training model (this may take a moment)...")
    # run training script
    subprocess.check_call([sys.executable, "-u", "backend/train.py"], cwd=str(ROOT))


def init_database():
    import sqlite3

    dbdir = DB_PATH.parent
    dbdir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            year INTEGER,
            fuel TEXT,
            transmission TEXT,
            km_driven INTEGER,
            owner_count INTEGER,
            engine_cc INTEGER,
            predicted_value REAL,
            lower_bound REAL,
            upper_bound REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def start_flask():
    app = Flask(__name__, static_folder="frontend/dist", static_url_path="")
    CORS(app)

    # load ML pipeline lazily
    from backend.ml import load_pipeline, predict_from_input, get_stats, get_available_cars, save_prediction

    pipeline = load_pipeline()

    @app.route("/api/predict", methods=["POST"])
    def predict():
        data = request.get_json() or {}
        try:
            result = predict_from_input(pipeline, data)
            save_prediction(DB_PATH, data, result)
            return jsonify({"success": True, "result": result})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route("/api/stats", methods=["GET"])
    def stats():
        return jsonify(get_stats(DB_PATH))

    @app.route("/api/cars", methods=["GET"])
    def cars():
        return jsonify(get_available_cars())

    # serve frontend
    @app.route("/", defaults={"path": "index.html"})
    @app.route("/<path:path>")
    def serve(path):
        dist = FRONTEND_DIR / "dist"
        if dist.exists():
            target = dist / path
            if target.exists():
                return send_from_directory(str(dist), path)
            else:
                # fallback to index.html for SPA routes
                return send_from_directory(str(dist), "index.html")
        return "Build not found. Please run the build.", 500

    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)


def open_browser_when_ready(url="http://127.0.0.1:5000"):
    # wait for server to be ready
    for _ in range(30):
        try:
            import requests

            r = requests.get(url)
            if r.status_code in (200, 404):
                webbrowser.open(url)
                return
        except Exception:
            pass
        time.sleep(1)
    webbrowser.open(url)


def main():
    # 1) install python requirements
    try:
        pip_install_requirements()
    except Exception as e:
        print("Warning: pip install failed:", e)

    # 2) train model if needed
    try:
        ensure_model_trained()
    except Exception as e:
        print("Model training failed:", e)

    # 3) init db
    init_database()

    # 4) npm install & build frontend
    try:
        npm_install_and_build()
    except Exception as e:
        print("Frontend build failed:", e)

    # 5) start flask in thread and open browser
    t = threading.Thread(target=start_flask, daemon=True)
    t.start()
    open_browser_when_ready()
    t.join()


if __name__ == "__main__":
    main()
