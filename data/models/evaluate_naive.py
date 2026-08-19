from pathlib import Path

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "demand_features.csv"
)


df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"],
)

df = df.sort_values(
    ["store_id", "product_id", "date"]
).reset_index(drop=True)


# ------------------------------------------------------------
# Test period
# ------------------------------------------------------------

test = df[
    df["date"] >= "2025-10-01"
].copy()


# ------------------------------------------------------------
# Naive prediction
# ------------------------------------------------------------

test["prediction"] = test["rolling_mean_7"]


test = test.dropna(
    subset=["prediction", "target_demand"]
)


# ------------------------------------------------------------
# Metrics
# ------------------------------------------------------------

mae = mean_absolute_error(
    test["target_demand"],
    test["prediction"],
)

rmse = mean_squared_error(
    test["target_demand"],
    test["prediction"],
) ** 0.5


print()
print("=" * 60)
print("NAIVE 7-DAY BASELINE")
print("=" * 60)

print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")