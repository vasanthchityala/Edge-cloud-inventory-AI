from pathlib import Path

import pandas as pd

from backend.app.database.session import SessionLocal
from backend.app.models.unified_priority import UnifiedPriority


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PRIORITY_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "unified_priority.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading unified priority data...")

df = pd.read_csv(PRIORITY_FILE)

print(
    f"Priority rows found: {len(df):,}"
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = {
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
}

missing_columns = (
    required_columns
    - set(df.columns)
)

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


# ============================================================
# DATABASE
# ============================================================

db = SessionLocal()

try:

    print()
    print("Removing existing unified priority records...")

    db.query(UnifiedPriority).delete()

    db.commit()

    print("Importing unified priority records...")

    records = []

    for _, row in df.iterrows():

        from_store_id = None

        if pd.notna(row["from_store_id"]):
            from_store_id = int(
                row["from_store_id"]
            )

        record = UnifiedPriority(
            store_id=int(row["store_id"]),
            product_id=int(row["product_id"]),
            category=str(row["category"]),
            current_stock=int(row["current_stock"]),
            safety_stock=int(row["safety_stock"]),
            forecast_demand=float(row["forecast_demand"]),
            risk_level=str(row["risk_level"]),
            edge_low_stock_count=int(
                row["edge_low_stock_count"]
            ),
            action=str(row["action"]),
            quantity=float(row["quantity"]),
            from_store_id=from_store_id,
            priority_score=float(
                row["priority_score"]
            ),
            unified_priority=str(
                row["unified_priority"]
            ),
        )

        records.append(record)

        if len(records) >= 500:

            db.add_all(records)

            db.commit()

            print(
                f"Imported {len(records):,} rows..."
            )

            records = []

    if records:

        db.add_all(records)

        db.commit()

        print(
            f"Imported {len(records):,} rows..."
        )


    # ========================================================
    # VERIFY
    # ========================================================

    count = (
        db.query(UnifiedPriority)
        .count()
    )

    print()
    print("=" * 60)
    print("UNIFIED PRIORITY IMPORT COMPLETE")
    print("=" * 60)

    print(
        f"Database priority rows: {count:,}"
    )

except Exception:

    db.rollback()

    raise

finally:

    db.close()