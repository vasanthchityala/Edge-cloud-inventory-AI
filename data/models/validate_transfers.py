from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

TRANSFER_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "optimized_transfers.csv"
)

RISK_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "inventory_risk.csv"
)


# ============================================================
# LOAD
# ============================================================

transfers = pd.read_csv(TRANSFER_PATH)
risk = pd.read_csv(RISK_PATH)


print()
print("=" * 60)
print("TRANSFER VALIDATION")
print("=" * 60)


# ============================================================
# 1. SELF TRANSFERS
# ============================================================

self_transfers = transfers[
    transfers["from_store_id"]
    == transfers["to_store_id"]
]

print(
    f"Self transfers: {len(self_transfers)}"
)


# ============================================================
# 2. INVALID QUANTITIES
# ============================================================

invalid_quantity = transfers[
    transfers["transfer_quantity"] <= 0
]

print(
    f"Invalid quantities: "
    f"{len(invalid_quantity)}"
)


# ============================================================
# 3. SOURCE STOCK CHECK
# ============================================================

source_check = transfers.merge(
    risk[
        [
            "store_id",
            "product_id",
            "current_stock",
            "safety_stock",
        ]
    ],
    left_on=[
        "from_store_id",
        "product_id",
    ],
    right_on=[
        "store_id",
        "product_id",
    ],
    how="left",
)

# Recalculate safe transferable stock.
source_check["available_for_transfer"] = (
    source_check["current_stock"]
    - source_check["safety_stock"]
).clip(lower=0)


invalid_source = source_check[
    source_check["transfer_quantity"]
    > source_check["available_for_transfer"]
]

print(
    f"Source stock violations: "
    f"{len(invalid_source)}"
)


# ============================================================
# 4. DESTINATION CAPACITY CHECK
# ============================================================

destination_check = transfers.merge(
    risk[
        [
            "store_id",
            "product_id",
            "current_stock",
            "capacity",
        ]
    ],
    left_on=[
        "to_store_id",
        "product_id",
    ],
    right_on=[
        "store_id",
        "product_id",
    ],
    how="left",
)

destination_check[
    "stock_after_transfer"
] = (
    destination_check["current_stock"]
    + destination_check["transfer_quantity"]
)

invalid_capacity = destination_check[
    destination_check["stock_after_transfer"]
    > destination_check["capacity"]
]

print(
    f"Capacity violations: "
    f"{len(invalid_capacity)}"
)


# ============================================================
# 5. DESTINATION RISK CHECK
# ============================================================

risk_check = transfers.merge(
    risk[
        [
            "store_id",
            "product_id",
            "risk_level",
        ]
    ],
    left_on=[
        "to_store_id",
        "product_id",
    ],
    right_on=[
        "store_id",
        "product_id",
    ],
    how="left",
)

invalid_destination = risk_check[
    risk_check["risk_level"] != "HIGH"
]

print(
    f"Non-high-risk destinations: "
    f"{len(invalid_destination)}"
)


# ============================================================
# 6. MISSING DATA CHECK
# ============================================================

missing_source = source_check[
    source_check["current_stock"].isna()
]

missing_destination = destination_check[
    destination_check["current_stock"].isna()
]

print(
    f"Missing source records: "
    f"{len(missing_source)}"
)

print(
    f"Missing destination records: "
    f"{len(missing_destination)}"
)


# ============================================================
# FINAL RESULT
# ============================================================

total_violations = (
    len(self_transfers)
    + len(invalid_quantity)
    + len(invalid_source)
    + len(invalid_capacity)
    + len(invalid_destination)
    + len(missing_source)
    + len(missing_destination)
)


print()
print("=" * 60)

if total_violations == 0:

    print("TRANSFER VALIDATION PASSED")

else:

    print("TRANSFER VALIDATION FAILED")

    print(
        f"Total violations: "
        f"{total_violations}"
    )

print("=" * 60)