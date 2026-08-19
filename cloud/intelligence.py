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

TRANSFER_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "optimized_transfers.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "cloud_action_plan.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading cloud intelligence data...")

risk = pd.read_csv(RISK_PATH)

transfers = pd.read_csv(
    TRANSFER_PATH
)


# ============================================================
# HIGH-RISK INVENTORY
# ============================================================

high_risk = risk[
    risk["risk_level"] == "HIGH"
].copy()


actions = []


# ============================================================
# BUILD FINAL ACTION
# ============================================================

for _, row in high_risk.iterrows():

    store_id = int(
        row["store_id"]
    )

    product_id = int(
        row["product_id"]
    )

    shortage = max(
        float(row["forecast_demand"])
        + float(row["safety_stock"])
        - float(row["current_stock"]),
        0,
    )

    # --------------------------------------------------------
    # Find transfer recommendation
    # --------------------------------------------------------

    matching_transfers = transfers[
        (transfers["to_store_id"] == store_id)
        &
        (transfers["product_id"] == product_id)
    ]

    if matching_transfers.empty:

        actions.append({
            "store_id": store_id,
            "product_id": product_id,
            "action": "RESTOCK_REQUIRED",
            "quantity": round(
                shortage,
                2,
            ),
            "from_store_id": None,
            "priority": "HIGH",
            "reason": (
                "Inventory shortage detected "
                "but no feasible store transfer "
                "was available."
            ),
        })

        continue

    # --------------------------------------------------------
    # Select best transfer
    # --------------------------------------------------------

    transfer = (
        matching_transfers
        .sort_values(
            "priority_score",
            ascending=False,
        )
        .iloc[0]
    )

    transfer_quantity = int(
        transfer["transfer_quantity"]
    )

    remaining_shortage = max(
        shortage
        - transfer_quantity,
        0,
    )

    # --------------------------------------------------------
    # Decide action status
    # --------------------------------------------------------

    if remaining_shortage <= 0:

        action = "TRANSFER"

        reason = (
            f"Transfer {transfer_quantity} "
            f"units from Store "
            f"{int(transfer['from_store_id'])} "
            f"to cover the forecasted shortage."
        )

    else:

        action = "PARTIAL_TRANSFER"

        reason = (
            f"Transfer {transfer_quantity} "
            f"units from Store "
            f"{int(transfer['from_store_id'])}. "
            f"Additional {remaining_shortage:.2f} "
            f"units are still required."
        )

    actions.append({
        "store_id": store_id,
        "product_id": product_id,
        "action": action,
        "quantity": transfer_quantity,
        "from_store_id": int(
            transfer["from_store_id"]
        ),
        "priority": "HIGH",
        "reason": reason,
    })


# ============================================================
# CREATE DATAFRAME
# ============================================================

action_plan = pd.DataFrame(
    actions
)


# ============================================================
# SORT
# ============================================================

if not action_plan.empty:

    action_plan = action_plan.sort_values(
        [
            "priority",
            "store_id",
            "product_id",
        ]
    ).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

action_plan.to_csv(
    OUTPUT_PATH,
    index=False,
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("CLOUD INTELLIGENCE")
print("=" * 60)

print(
    f"High-risk items: "
    f"{len(high_risk):,}"
)

print(
    f"Final actions: "
    f"{len(action_plan):,}"
)

if not action_plan.empty:

    print()
    print("Action distribution:")

    print(
        action_plan[
            "action"
        ].value_counts()
    )

    print()
    print("Top 10 actions:")

    print(
        action_plan
        .head(10)
        .to_string(index=False)
    )


print()
print("Saved to:")
print(OUTPUT_PATH)