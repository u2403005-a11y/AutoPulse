"""
Train script for used car price model. Generates a synthetic dataset if needed,
trains a RandomForestRegressor pipeline and saves it to model/model.joblib
"""
import joblib
from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).parent.parent
MODEL_DIR = ROOT / "model"
DATA_FILE = MODEL_DIR / "dataset.csv"


def generate_synthetic_dataset(path: Path, n=2000):
    import random
    brands = {
        "Tesla": ["Model S", "Model 3", "Model X", "Model Y"],
        "Porsche": ["911", "Cayenne", "Panamera"],
        "Bugatti": ["Chiron"],
        "Audi": ["A4", "A6", "Q7"],
        "BMW": ["3 Series", "5 Series", "X5"],
        "Mercedes": ["C Class", "E Class", "GLE"],
    }
    fuels = ["Petrol", "Diesel", "Electric", "Hybrid"]
    transmissions = ["Manual", "Automatic"]

    rows = []
    for _ in range(n):
        brand = random.choice(list(brands.keys()))
        model = random.choice(brands[brand])
        year = random.randint(2005, 2022)
        fuel = random.choice(fuels)
        transmission = random.choice(transmissions)
        km = max(1000, int(np.random.exponential(30000)))
        owner = random.randint(0, 3)
        engine = random.choice([1000, 1500, 2000, 3000, 4000])

        # base price influenced by brand and model
        base = 20000
        if brand == "Bugatti":
            base = 2500000
        elif brand == "Porsche":
            base = 90000
        elif brand == "Tesla":
            base = 70000
        elif brand in ("BMW", "Mercedes"):
            base = 45000
        elif brand == "Audi":
            base = 40000

        age = 2023 - year
        price = base * (0.95 ** age) - (km * 0.02) - (owner * 2000) + (engine / 10)
        price = max(1000, price + np.random.normal(0, base * 0.05))

        rows.append({
            "brand": brand,
            "model": model,
            "year": year,
            "fuel": fuel,
            "transmission": transmission,
            "km_driven": km,
            "owner_count": owner,
            "engine_cc": engine,
            "price": round(price, 2),
        })

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return df


def train():
    MODEL_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        print("Generating synthetic dataset...")
        df = generate_synthetic_dataset(DATA_FILE)
    else:
        df = pd.read_csv(DATA_FILE)

    X = df.drop(columns=["price"])
    y = df["price"]

    categorical = ["brand", "model", "fuel", "transmission"]
    numeric = ["year", "km_driven", "owner_count", "engine_cc"]

    preproc = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", StandardScaler(), numeric),
    ])

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    pipeline = Pipeline([("preproc", preproc), ("model", model)])
    pipeline.fit(X, y)

    joblib.dump(pipeline, MODEL_DIR / "model.joblib")
    print("Model trained and saved to model/model.joblib")


if __name__ == "__main__":
    train()
