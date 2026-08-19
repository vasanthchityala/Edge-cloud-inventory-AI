from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

FORECAST_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecast_results.csv"
)


df = pd.read_csv(
    FORECAST_PATH,
    parse_dates=["date"],
)


# ============================================================
# OVERALL ERROR
# ============================================================

print()
print("=" * 60)
print("FORECAST ERROR ANALYSIS")
print("=" * 60)

print(f"Mean absolute error: {df['absolute_error'].mean():.4f}")
print(f"Maximum error:       {df['absolute_error'].max():.4f}")


# ============================================================
# WORST FORECASTS
# ============================================================

print()
print("=" * 60)
print("TOP 10 WORST FORECASTS")
print("=" * 60)

worst = df.nlargest(
    10,
    "absolute_error",
)

print(
    worst[
        [
            "date",
            "store_id",
            "product_id",
            "target_demand",
            "predicted_demand",
            "absolute_error",
        ]
    ].to_string(index=False)
)


# ============================================================
# ERROR BY CATEGORY
# ============================================================

category_error = (
    df.groupby("category")["absolute_error"]
    .mean()
    .sort_values(ascending=False)
)

print()
print("=" * 60)
print("ERROR BY CATEGORY")
print("=" * 60)

print(category_error)


# ============================================================
# ERROR BY STORE
# ============================================================

store_error = (
    df.groupby("store_id")["absolute_error"]
    .mean()
    .sort_values(ascending=False)
)

print()
print("=" * 60)
print("ERROR BY STORE")
print("=" * 60)

print(store_error.head(10))


# ============================================================
# UNDER / OVER PREDICTION
# ============================================================

df["prediction_type"] = "Correct"

df.loc[
    df["predicted_demand"] < df["target_demand"],
    "prediction_type"
] = "Underprediction"

df.loc[
    df["predicted_demand"] > df["target_demand"],
    "prediction_type"
] = "Overprediction"


prediction_counts = (
    df["prediction_type"]
    .value_counts()
)

print()
print("=" * 60)
print("PREDICTION DIRECTION")
print("=" * 60)

print(prediction_counts)


# ============================================================
# SAVE SUMMARY
# ============================================================

summary = pd.DataFrame({
    "metric": [
        "mean_absolute_error",
        "maximum_absolute_error",
        "underpredictions",
        "overpredictions",
    ],
    "value": [
        df["absolute_error"].mean(),
        df["absolute_error"].max(),
        (
            df["prediction_type"]
            == "Underprediction"
        ).sum(),
        (
            df["prediction_type"]
            == "Overprediction"
        ).sum(),
    ],
})

summary.to_csv(
    BASE_DIR
    / "data"
    / "processed"
    / "forecast_analysis_summary.csv",
    index=False,
)


print()
print("Analysis saved successfully.")