from pathlib import Path

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
# CALCULATE SOURCE AVAILABILITY
# ============================================================

# A source store must keep its safety stock.
df["available_for_transfer"] = (
    df["current_stock"]
    - df["safety_stock"]
).clip(lower=0)


# ============================================================
# CALCULATE DESTINATION SHORTAGE
# ============================================================

df["shortage"] = (
    df["forecast_demand"]
    + df["safety_stock"]
    - df["current_stock"]
).clip(lower=0)


# ============================================================
# SOURCE STORES
# ============================================================

sources = df[
    df["available_for_transfer"] > 0
].copy()


# ============================================================
# DESTINATION STORES
# ============================================================

destinations = df[
    df["risk_level"] == "HIGH"
].copy()


recommendations = []


# ============================================================
# OPTIMIZATION
# ============================================================

for _, destination in destinations.iterrows():

    product_id = int(destination["product_id"])
    destination_store = int(
        destination["store_id"]
    )

    shortage = float(
        destination["shortage"]
    )

    if shortage <= 0:
        continue

    # Find stores having the same product.
    candidates = sources[
        (sources["product_id"] == product_id)
        &
        (
            sources["store_id"]
            != destination_store
        )
    ].copy()

    # Prefer stores with the largest safe surplus.
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

        if available <= 0:
            continue

        # Destination capacity check.
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

        if capacity_available <= 0:
            continue

        transfer_quantity = min(
            available,
            remaining_shortage,
            capacity_available,
        )

        transfer_quantity = int(
            transfer_quantity
        )

        if transfer_quantity <= 0:
            continue

        # ----------------------------------------------------
        # Priority score
        # ----------------------------------------------------

        shortage_ratio = (
            shortage
            / max(
                destination["safety_stock"],
                1,
            )
        )

        priority = min(
            shortage_ratio,
            10,
        )

        recommendations.append({
            "product_id": product_id,
            "from_store_id": int(
                source["store_id"]
            ),
            "to_store_id": destination_store,
            "transfer_quantity": transfer_quantity,
            "destination_shortage": round(
                shortage,
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

        remaining_shortage -= (
            transfer_quantity
        )


# ============================================================
# CREATE RESULT
# ============================================================

result = pd.DataFrame(
    recommendations
)


# ============================================================
# SORT BY PRIORITY
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

else:

    print(
        "No feasible transfers found."
    )


print()
print("Saved to:")
print(OUTPUT_PATH)