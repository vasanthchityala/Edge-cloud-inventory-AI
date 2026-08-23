from pathlib import Path
from datetime import datetime

import pandas as pd

from backend.app.database.session import SessionLocal
from backend.app.models.inventory_risk import InventoryRisk


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RISK_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "inventory_risk.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading inventory risk data...")

df = pd.read_csv(RISK_FILE)

print(
    f"Risk rows found: {len(df):,}"
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = {
    "date",
    "store_id",
    "product_id",
    "category",
    "target_demand",
    "predicted_demand",
    "forecast_error",
    "absolute_error",
    "current_stock",
    "safety_stock",
    "capacity",
    "lead_time_days",
    "forecast_demand",
    "projected_stock",
    "required_stock",
    "stock_surplus",
    "risk_level",
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
    print("Removing existing inventory-risk records...")

    db.query(InventoryRisk).delete()

    db.commit()

    print("Importing inventory-risk records...")

    records = []

    for _, row in df.iterrows():

        record = InventoryRisk(
            date=datetime.strptime(
                str(row["date"]),
                "%Y-%m-%d",
            ).date(),

            store_id=int(
                row["store_id"]
            ),

            product_id=int(
                row["product_id"]
            ),

            category=str(
                row["category"]
            ),

            target_demand=float(
                row["target_demand"]
            ),

            predicted_demand=float(
                row["predicted_demand"]
            ),

            forecast_error=float(
                row["forecast_error"]
            ),

            absolute_error=float(
                row["absolute_error"]
            ),

            current_stock=int(
                row["current_stock"]
            ),

            safety_stock=int(
                row["safety_stock"]
            ),

            capacity=int(
                row["capacity"]
            ),

            lead_time_days=int(
                row["lead_time_days"]
            ),

            forecast_demand=float(
                row["forecast_demand"]
            ),

            projected_stock=float(
                row["projected_stock"]
            ),

            required_stock=float(
                row["required_stock"]
            ),

            stock_surplus=float(
                row["stock_surplus"]
            ),

            risk_level=str(
                row["risk_level"]
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

    # ========================================================
    # VERIFY
    # ========================================================

    count = (
        db.query(InventoryRisk)
        .count()
    )

    print()
    print("=" * 60)
    print("INVENTORY RISK IMPORT COMPLETE")
    print("=" * 60)

    print(
        f"Database risk rows: {count:,}"
    )

except Exception:

    db.rollback()

    raise

finally:

    db.close()