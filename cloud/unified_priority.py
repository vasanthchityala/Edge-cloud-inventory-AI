from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

RISK_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "inventory_risk.csv"
)

EDGE_INVENTORY_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "inventory.csv"
)

ACTION_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "cloud_action_plan.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "unified_priority.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading Edge and Cloud data...")

risk = pd.read_csv(RISK_PATH)

inventory = pd.read_csv(
    EDGE_INVENTORY_PATH
)

actions = pd.read_csv(
    ACTION_PATH
)


# ============================================================
# CREATE EDGE SIGNALS
# ============================================================

inventory["edge_low_stock"] = (
    inventory["current_stock"]
    < inventory["safety_stock"]
)

edge_summary = (
    inventory
    .groupby("store_id")
    .agg(
        edge_low_stock_count=(
            "edge_low_stock",
            "sum",
        )
    )
    .reset_index()
)


# ============================================================
# MERGE EDGE + ML RISK
# ============================================================

unified = risk.merge(
    edge_summary,
    on="store_id",
    how="left",
)


unified["edge_low_stock_count"] = (
    unified["edge_low_stock_count"]
    .fillna(0)
)


# ============================================================
# MERGE CLOUD ACTION
# ============================================================

unified = unified.merge(
    actions[
        [
            "store_id",
            "product_id",
            "action",
            "quantity",
            "from_store_id",
        ]
    ],
    on=[
        "store_id",
        "product_id",
    ],
    how="left",
)


# ============================================================
# PRIORITY SCORE
# ============================================================

def calculate_priority(row):

    score = 0

    # --------------------------------------------------------
    # ML risk
    # --------------------------------------------------------

    if row["risk_level"] == "HIGH":
        score += 50

    elif row["risk_level"] == "MEDIUM":
        score += 25

    # --------------------------------------------------------
    # Edge signal
    # --------------------------------------------------------

    if row["edge_low_stock_count"] >= 20:
        score += 30

    elif row["edge_low_stock_count"] >= 10:
        score += 15

    elif row["edge_low_stock_count"] > 0:
        score += 5

    # --------------------------------------------------------
    # Forecast shortage
    # --------------------------------------------------------

    shortage = max(
        row["forecast_demand"]
        + row["safety_stock"]
        - row["current_stock"],
        0,
    )

    if shortage >= 100:
        score += 20

    elif shortage >= 50:
        score += 15

    elif shortage > 0:
        score += 10

    return score


unified["priority_score"] = (
    unified.apply(
        calculate_priority,
        axis=1,
    )
)


# ============================================================
# PRIORITY CLASSIFICATION
# ============================================================

def classify_priority(score):

    if score >= 80:
        return "CRITICAL"

    if score >= 50:
        return "HIGH"

    if score >= 25:
        return "MEDIUM"

    return "LOW"


unified["unified_priority"] = (
    unified["priority_score"]
    .apply(classify_priority)
)


# ============================================================
# SAVE
# ============================================================

columns = [
    "store_id",
    "product_id",
    "category",
    "current_stock",
    "safety_stock",
    "forecast_demand",
    "risk_level",
    "edge_low_stock_count",
    "action",
    "quantity",
    "from_store_id",
    "priority_score",
    "unified_priority",
]

result = unified[columns].copy()

result = result.sort_values(
    "priority_score",
    ascending=False,
).reset_index(drop=True)


result.to_csv(
    OUTPUT_PATH,
    index=False,
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("UNIFIED EDGE-CLOUD PRIORITY")
print("=" * 60)

print(
    f"Records analyzed: "
    f"{len(result):,}"
)

print()
print("Priority distribution:")

print(
    result[
        "unified_priority"
    ].value_counts()
)


print()
print("Top 10 priority items:")

print(
    result.head(10).to_string(
        index=False
    )
)


print()
print("Saved to:")
print(OUTPUT_PATH)