from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "demand_features.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "data"
    / "models"
    / "gradient_boosting_demand_model.joblib"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecast_results.csv"
)


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "store_id",
    "product_id",
    "price",
    "promotion",
    "is_weekend",
    "is_holiday",
    "day_of_week",
    "day_of_month",
    "week_of_year",
    "month",
    "quarter",
    "year",
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_14",
    "rolling_mean_28",
    "rolling_std_7",
    "price_change",
]


# ============================================================
# LOAD DATA AND MODEL
# ============================================================

print("Loading data...")

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"],
)

model = joblib.load(MODEL_PATH)


# ============================================================
# TEST DATA
# ============================================================

test = df[
    df["date"] >= "2025-10-01"
].copy()

test = test.dropna(
    subset=FEATURES
).copy()


# ============================================================
# PREDICTION
# ============================================================

print("Generating forecasts...")

test["predicted_demand"] = model.predict(
    test[FEATURES]
)

# Demand cannot be negative
test["predicted_demand"] = (
    test["predicted_demand"]
    .clip(lower=0)
)

test["forecast_error"] = (
    test["target_demand"]
    - test["predicted_demand"]
)

test["absolute_error"] = (
    test["forecast_error"]
    .abs()
)


# ============================================================
# SELECT OUTPUT COLUMNS
# ============================================================

results = test[
    [
        "date",
        "store_id",
        "product_id",
        "category",
        "target_demand",
        "predicted_demand",
        "forecast_error",
        "absolute_error",
    ]
].copy()


# ============================================================
# SAVE
# ============================================================

results.to_csv(
    OUTPUT_PATH,
    index=False,
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("FORECAST GENERATION COMPLETE")
print("=" * 60)

print(f"Forecast rows: {len(results):,}")

print()
print("Sample forecasts:")

print(
    results.head(10).to_string(
        index=False
    )
)

print()
print("Saved to:")

print(OUTPUT_PATH)