from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "processed" / "demand_features.csv"
MODEL_DIR = BASE_DIR / "data" / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading ML dataset...")

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"],
)

df = df.sort_values("date").reset_index(drop=True)


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

TARGET = "target_demand"


# ============================================================
# REMOVE INVALID VALUES
# ============================================================

df = df.dropna(
    subset=FEATURES + [TARGET]
).copy()


# ============================================================
# TIME-BASED SPLIT
# ============================================================

train = df[
    df["date"] < "2025-07-01"
]

validation = df[
    (df["date"] >= "2025-07-01")
    & (df["date"] < "2025-10-01")
]

test = df[
    df["date"] >= "2025-10-01"
]


print()
print("=" * 60)
print("DATA SPLIT")
print("=" * 60)

print(f"Training:   {len(train):,}")
print(f"Validation: {len(validation):,}")
print(f"Test:       {len(test):,}")


# ============================================================
# TRAIN
# ============================================================

X_train = train[FEATURES]
y_train = train[TARGET]

X_validation = validation[FEATURES]
y_validation = validation[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]


print()
print("Training Random Forest...")


model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
)


model.fit(
    X_train,
    y_train,
)


# ============================================================
# VALIDATION
# ============================================================

validation_predictions = model.predict(
    X_validation
)

validation_mae = mean_absolute_error(
    y_validation,
    validation_predictions,
)

validation_rmse = mean_squared_error(
    y_validation,
    validation_predictions,
) ** 0.5


print()
print("=" * 60)
print("VALIDATION RESULTS")
print("=" * 60)

print(f"MAE:  {validation_mae:.4f}")
print(f"RMSE: {validation_rmse:.4f}")


# ============================================================
# TEST
# ============================================================

test_predictions = model.predict(
    X_test
)

test_mae = mean_absolute_error(
    y_test,
    test_predictions,
)

test_rmse = mean_squared_error(
    y_test,
    test_predictions,
) ** 0.5


print()
print("=" * 60)
print("TEST RESULTS")
print("=" * 60)

print(f"MAE:  {test_mae:.4f}")
print(f"RMSE: {test_rmse:.4f}")


# ============================================================
# SAVE MODEL
# ============================================================

model_path = MODEL_DIR / "baseline_random_forest.joblib"

joblib.dump(
    model,
    model_path,
)


print()
print("=" * 60)
print("MODEL SAVED")
print("=" * 60)

print(model_path)