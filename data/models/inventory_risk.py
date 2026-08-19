from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

FORECAST_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecast_results.csv"
)

INVENTORY_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "inventory.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "inventory_risk.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading forecast and inventory data...")

forecast = pd.read_csv(
    FORECAST_PATH,
    parse_dates=["date"],
)

inventory = pd.read_csv(
    INVENTORY_PATH
)


# ============================================================
# GET RECENT FORECAST
# ============================================================

latest_date = forecast["date"].max()

latest_forecast = forecast[
    forecast["date"] == latest_date
].copy()


# ============================================================
# MERGE INVENTORY + FORECAST
# ============================================================

risk = latest_forecast.merge(
    inventory,
    on=["store_id", "product_id"],
    how="left",
)


# ============================================================
# RISK CALCULATIONS
# ============================================================

risk["forecast_demand"] = (
    risk["predicted_demand"].round(2)
)

risk["projected_stock"] = (
    risk["current_stock"]
    - risk["forecast_demand"]
)

risk["required_stock"] = (
    risk["forecast_demand"]
    + risk["safety_stock"]
)

risk["stock_surplus"] = (
    risk["current_stock"]
    - risk["required_stock"]
)


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def classify_risk(row):

    if row["current_stock"] <= 0:
        return "OUT_OF_STOCK"

    if row["projected_stock"] < 0:
        return "HIGH"

    if row["projected_stock"] < row["safety_stock"]:
        return "MEDIUM"

    if row["stock_surplus"] > (
        row["capacity"] * 0.5
    ):
        return "EXCESS"

    return "LOW"


risk["risk_level"] = risk.apply(
    classify_risk,
    axis=1,
)


# ============================================================
# SAVE
# ============================================================

risk.to_csv(
    OUTPUT_PATH,
    index=False,
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("INVENTORY RISK ANALYSIS")
print("=" * 60)

print(f"Forecast date: {latest_date}")
print(f"Products analyzed: {len(risk):,}")

print()
print("Risk distribution:")

print(
    risk["risk_level"]
    .value_counts()
)


print()
print("Highest-risk inventory:")

print(
    risk[
        [
            "store_id",
            "product_id",
            "current_stock",
            "forecast_demand",
            "safety_stock",
            "projected_stock",
            "risk_level",
        ]
    ]
    .sort_values(
        "projected_stock"
    )
    .head(10)
    .to_string(index=False)
)


print()
print(f"Saved to:")
print(OUTPUT_PATH)