from pathlib import Path

import pandas as pd


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
    / "transfer_recommendations.csv"
)


# ============================================================
# LOAD RISK DATA
# ============================================================

print("Loading inventory risk data...")

df = pd.read_csv(RISK_PATH)


# ============================================================
# CALCULATE SURPLUS / SHORTAGE
# ============================================================

df["surplus"] = (
    df["current_stock"]
    - df["required_stock"]
)

df["shortage"] = (
    -df["projected_stock"]
).clip(lower=0)


# ============================================================
# FIND HIGH-RISK DESTINATIONS
# ============================================================

destinations = df[
    df["risk_level"] == "HIGH"
].copy()


# ============================================================
# FIND EXCESS SOURCES
# ============================================================

sources = df[
    df["surplus"] > 0
].copy()


recommendations = []


# ============================================================
# MATCH SOURCE → DESTINATION
# ============================================================

for _, destination in destinations.iterrows():

    product_id = destination["product_id"]

    shortage = destination["shortage"]

    if shortage <= 0:
        continue

    possible_sources = sources[
        (sources["product_id"] == product_id)
        &
        (sources["store_id"] != destination["store_id"])
    ].copy()

    possible_sources = possible_sources.sort_values(
        "surplus",
        ascending=False,
    )

    remaining = shortage

    for _, source in possible_sources.iterrows():

        if remaining <= 0:
            break

        available = source["surplus"]

        transfer_quantity = min(
            available,
            remaining,
        )

        if transfer_quantity <= 0:
            continue

        recommendations.append({
            "product_id": int(product_id),
            "from_store_id": int(
                source["store_id"]
            ),
            "to_store_id": int(
                destination["store_id"]
            ),
            "transfer_quantity": int(
                transfer_quantity
            ),
            "destination_shortage": round(
                shortage,
                2,
            ),
        })

        remaining -= transfer_quantity


# ============================================================
# CREATE RESULT
# ============================================================

recommendations_df = pd.DataFrame(
    recommendations
)


# ============================================================
# SAVE
# ============================================================

recommendations_df.to_csv(
    OUTPUT_PATH,
    index=False,
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("REBALANCING ANALYSIS")
print("=" * 60)

print(
    f"Transfer recommendations: "
    f"{len(recommendations_df):,}"
)

if not recommendations_df.empty:

    print()
    print("Top recommendations:")

    print(
        recommendations_df
        .head(10)
        .to_string(index=False)
    )

else:

    print(
        "No valid transfer recommendations found."
    )


print()
print("Saved to:")
print(OUTPUT_PATH)