from pathlib import Path

import math
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

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
    / "optimized_transfers.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading inventory risk data...")

df = pd.read_csv(RISK_PATH)


# ============================================================
# SOURCE AVAILABILITY
# ============================================================

# Source store must keep its safety stock.
df["available_for_transfer"] = (
    df["current_stock"]
    - df["safety_stock"]
).clip(lower=0)


# ============================================================
# DESTINATION SHORTAGE
# ============================================================

# Required inventory =
# forecast demand + safety stock
#
# Shortage =
# required inventory - current inventory

df["required_stock"] = (
    df["forecast_demand"]
    + df["safety_stock"]
)

df["shortage"] = (
    df["required_stock"]
    - df["current_stock"]
).clip(lower=0)


# ============================================================
# SOURCE STORES
# ============================================================

sources = df[
    df["available_for_transfer"] >= 1
].copy()


# ============================================================
# DESTINATION STORES
# ============================================================

destinations = df[
    df["risk_level"] == "HIGH"
].copy()


recommendations = []


# ============================================================
# MATCH SOURCES TO DESTINATIONS
# ============================================================

for _, destination in destinations.iterrows():

    product_id = int(
        destination["product_id"]
    )

    destination_store = int(
        destination["store_id"]
    )

    shortage = float(
        destination["shortage"]
    )

    if shortage <= 0:
        continue

    # --------------------------------------------------------
    # Find stores with same product
    # --------------------------------------------------------

    candidates = sources[
        (sources["product_id"] == product_id)
        &
        (
            sources["store_id"]
            != destination_store
        )
    ].copy()

    # Largest safe surplus first.
    candidates = candidates.sort_values(
        "available_for_transfer",
        ascending=False,
    )

    remaining_shortage = shortage

    for _, source in candidates.iterrows():

        if remaining_shortage <= 0:
            break

        available = float(
            source["available_for_transfer"]
        )

        if available < 1:
            continue

        # ----------------------------------------------------
        # Destination capacity
        # ----------------------------------------------------

        destination_capacity = float(
            destination["capacity"]
        )

        destination_stock = float(
            destination["current_stock"]
        )

        capacity_available = max(
            destination_capacity
            - destination_stock,
            0,
        )

        if capacity_available < 1:
            continue

        # ----------------------------------------------------
        # Maximum feasible transfer
        # ----------------------------------------------------

        maximum_transfer = min(
            available,
            remaining_shortage,
            capacity_available,
        )

        # Physical inventory must be whole units.
        transfer_quantity = math.floor(
            maximum_transfer
        )

        if transfer_quantity <= 0:
            continue

        # ----------------------------------------------------
        # Priority
        # ----------------------------------------------------

        shortage_ratio = (
            shortage
            / max(
                float(destination["safety_stock"]),
                1,
            )
        )

        priority = min(
            shortage_ratio,
            10,
        )

        # ----------------------------------------------------
        # Remaining shortage after transfer
        # ----------------------------------------------------

        remaining_after_transfer = max(
            remaining_shortage
            - transfer_quantity,
            0,
        )

        recommendations.append({
            "product_id": product_id,

            "from_store_id": int(
                source["store_id"]
            ),

            "to_store_id": destination_store,

            "transfer_quantity": int(
                transfer_quantity
            ),

            "destination_shortage": round(
                shortage,
                2,
            ),

            "remaining_shortage": round(
                remaining_after_transfer,
                2,
            ),

            "source_available": round(
                available,
                2,
            ),

            "destination_capacity": int(
                destination_capacity
            ),

            "priority_score": round(
                priority,
                2,
            ),
        })

        remaining_shortage = (
            remaining_after_transfer
        )


# ============================================================
# CREATE RESULT
# ============================================================

result = pd.DataFrame(
    recommendations
)


# ============================================================
# SORT
# ============================================================

if not result.empty:

    result = result.sort_values(
        [
            "priority_score",
            "destination_shortage",
        ],
        ascending=False,
    ).reset_index(drop=True)


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
print("TRANSFER OPTIMIZATION COMPLETE")
print("=" * 60)

print(
    f"Optimized recommendations: "
    f"{len(result):,}"
)

if not result.empty:

    print()
    print("Top optimized transfers:")

    print(
        result.head(10).to_string(
            index=False
        )
    )

    print()

    print(
        "Total units recommended:",
        int(
            result[
                "transfer_quantity"
            ].sum()
        ),
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

else:

    print(
        "No feasible transfers found."
    )


print()
print("Saved to:")
print(OUTPUT_PATH)