from pathlib import Path
import joblib
import pandas as pd
import numpy as np

ROOT = Path(__file__).parent.parent
MODEL_DIR = ROOT / "model"
MODEL_FILE = MODEL_DIR / "model.joblib"


def load_pipeline():
    if not MODEL_FILE.exists():
        raise FileNotFoundError("Model not found. Please run training.")
    pipeline = joblib.load(MODEL_FILE)
    return pipeline


def predict_from_input(pipeline, data: dict):
    # expected keys: brand, model, year, fuel, transmission, km_driven, owner_count, engine_cc
    df = pd.DataFrame([{
        "brand": data.get("brand", "Tesla"),
        "model": data.get("model", "Model 3"),
        "year": int(data.get("year", 2018)),
        "fuel": data.get("fuel", "Petrol"),
        "transmission": data.get("transmission", "Automatic"),
        "km_driven": int(data.get("km_driven", 20000)),
        "owner_count": int(data.get("owner_count", 1)),
        "engine_cc": int(data.get("engine_cc", 2000)),
    }])

    preds = pipeline.predict(df)
    # get estimator-wise predictions for uncertainty
    try:
        model = pipeline.named_steps["model"]
        preproc = pipeline.named_steps["preproc"]
        X_trans = preproc.transform(df)
        all_preds = np.vstack([est.predict(X_trans) for est in model.estimators_])
        std = float(np.std(all_preds))
    except Exception:
        std = 0.0

    pred = float(preds[0])
    lower = pred - 1.96 * std
    upper = pred + 1.96 * std

    return {
        "predicted_value": round(pred, 2),
        "lower_bound": round(max(0, lower), 2),
        "upper_bound": round(upper, 2),
        "std": round(std, 2),
    }


def save_prediction(db_path, data: dict, result: dict):
    import sqlite3

    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO predictions (brand, model, year, fuel, transmission, km_driven, owner_count, engine_cc, predicted_value, lower_bound, upper_bound)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("brand"),
            data.get("model"),
            int(data.get("year") or 0),
            data.get("fuel"),
            data.get("transmission"),
            int(data.get("km_driven") or 0),
            int(data.get("owner_count") or 0),
            int(data.get("engine_cc") or 0),
            result.get("predicted_value"),
            result.get("lower_bound"),
            result.get("upper_bound"),
        ),
    )
    conn.commit()
    conn.close()


def get_stats(db_path):
    import sqlite3

    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("SELECT COUNT(*), AVG(predicted_value) FROM predictions")
    row = c.fetchone()
    total = row[0] or 0
    avg = round(row[1] or 0, 2)
    c.execute("SELECT brand, COUNT(*) as cnt FROM predictions GROUP BY brand ORDER BY cnt DESC LIMIT 5")
    popular = [{"brand": r[0], "count": r[1]} for r in c.fetchall()]
    conn.close()
    return {"total": total, "average": avg, "popular_brands": popular}


def get_available_cars():
    # read from dataset if available
    ds = MODEL_DIR / "dataset.csv"
    if not ds.exists():
        return {"brands": [], "models": []}
    import pandas as pd

    df = pd.read_csv(ds)
    brands = sorted(df["brand"].unique().tolist())
    models = df.groupby("brand")["model"].unique().apply(list).to_dict()
    return {"brands": brands, "models": models}
