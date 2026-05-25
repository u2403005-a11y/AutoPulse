import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory # type: ignore
from flask_cors import CORS # type: ignore

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).parent
FRONTEND_DIR = ROOT / "frontend"
MODEL_DIR = ROOT / "model"
DB_PATH = ROOT / "database" / "predictions.db"

# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR / "dist"),
    static_url_path=""
)

CORS(app)

# =========================================================
# DATABASE INIT
# =========================================================

def init_database():
    import sqlite3

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("""
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
    """)

    conn.commit()
    conn.close()

# =========================================================
# LOAD ML PIPELINE
# =========================================================

from backend.ml import (
    load_pipeline,
    predict_from_input,
    get_stats,
    get_available_cars,
    save_prediction
)

pipeline = load_pipeline()

# =========================================================
# API ROUTES
# =========================================================

@app.route("/api/predict", methods=["POST"])
def predict():

    data = request.get_json() or {}

    try:
        result = predict_from_input(pipeline, data)

        save_prediction(DB_PATH, data, result)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify(get_stats(DB_PATH))


@app.route("/api/cars", methods=["GET"])
def cars():
    return jsonify(get_available_cars())

# =========================================================
# FRONTEND SERVING
# =========================================================

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve(path):

    dist_folder = FRONTEND_DIR / "dist"

    if not dist_folder.exists():
        return "Frontend build not found. Run npm run build inside frontend folder.", 500

    requested_file = dist_folder / path

    # Serve actual file
    if requested_file.exists():
        return send_from_directory(str(dist_folder), path)

    # SPA fallback
    return send_from_directory(str(dist_folder), "index.html")

# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    init_database()

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )