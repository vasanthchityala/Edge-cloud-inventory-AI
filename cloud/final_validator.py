from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

ACTION_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "cloud_action_plan.csv"
)

RISK_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "inventory_risk.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "validated_action_plan.csv"
)


# ============================================================
# LOAD
# ============================================================

print("Loading final decision data...")

actions = pd.read_csv(
    ACTION_PATH
)

risk = pd.read_csv(
    RISK_PATH
)


# ============================================================
# MERGE
# ============================================================

result = actions.merge(
    risk[
        [
            "store_id",
            "product_id",
            "current_stock",
            "safety_stock",
            "capacity",
            "forecast_demand",
        ]
    ],
    on=[
        "store_id",
        "product_id",
    ],
    how="left",
)


# ============================================================
# VALIDATION COLUMNS
# ============================================================

result["validation_status"] = "VALID"

result["validation_reason"] = (
    "All hard constraints satisfied."
)


result["required_stock"] = (
    result["forecast_demand"]
    + result["safety_stock"]
)

result["stock_after_transfer"] = (
    result["current_stock"]
    + result["quantity"]
)

result["remaining_shortage"] = (
    result["required_stock"]
    - result["stock_after_transfer"]
).clip(lower=0)


# ============================================================
# VALIDATE EACH ACTION
# ============================================================

for index, row in result.iterrows():

    action = row["action"]

    quantity = float(
        row["quantity"]
    )

    current_stock = float(
        row["current_stock"]
    )

    capacity = float(
        row["capacity"]
    )

    stock_after = float(
        row["stock_after_transfer"]
    )

    remaining = float(
        row["remaining_shortage"]
    )

    # --------------------------------------------------------
    # Quantity check
    # --------------------------------------------------------

    if quantity <= 0:

        result.loc[
            index,
            "validation_status"
        ] = "INVALID"

        result.loc[
            index,
            "validation_reason"
        ] = (
            "Transfer quantity must be positive."
        )

        continue

    # --------------------------------------------------------
    # Capacity check
    # --------------------------------------------------------

    if stock_after > capacity:

        result.loc[
            index,
            "validation_status"
        ] = "INVALID"

        result.loc[
            index,
            "validation_reason"
        ] = (
            "Destination capacity exceeded."
        )

        continue

    # --------------------------------------------------------
    # Partial transfer
    # --------------------------------------------------------

    if action == "PARTIAL_TRANSFER":

        result.loc[
            index,
            "validation_status"
        ] = "PARTIAL"

        result.loc[
            index,
            "validation_reason"
        ] = (
            f"Hard constraints satisfied, "
            f"but {remaining:.2f} units "
            f"remain uncovered."
        )

        continue

    # --------------------------------------------------------
    # Full transfer
    # --------------------------------------------------------

    if action == "TRANSFER":

        if remaining > 0:

            result.loc[
                index,
                "validation_status"
            ] = "PARTIAL"

            result.loc[
                index,
                "validation_reason"
            ] = (
                f"Transfer is feasible, "
                f"but {remaining:.2f} units "
                f"remain uncovered."
            )

        else:

            result.loc[
                index,
                "validation_status"
            ] = "VALID"

            result.loc[
                index,
                "validation_reason"
            ] = (
                "Transfer fully covers "
                "forecast demand and safety stock."
            )

        continue

    # --------------------------------------------------------
    # Restock
    # --------------------------------------------------------

    if action == "RESTOCK_REQUIRED":

        result.loc[
            index,
            "validation_status"
        ] = "RESTOCK"

        result.loc[
            index,
            "validation_reason"
        ] = (
            "No feasible store transfer "
            "was available."
        )


# ============================================================
# SAVE
# ============================================================

result.to_csv(
    OUTPUT_PATH,
    index=False,
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("FINAL DECISION VALIDATION")
print("=" * 60)

print(
    f"Total actions: "
    f"{len(result):,}"
)

print()
print("Validation status:")

print(
    result[
        "validation_status"
    ].value_counts()
)

print()
print("Validation reasons:")

print(
    result[
        "validation_reason"
    ].value_counts()
)

print()
print(
    "Total remaining shortage:",
    round(
        result[
            "remaining_shortage"
        ].sum(),
        2,
    ),
)

print()
print("Saved to:")
print(OUTPUT_PATH)