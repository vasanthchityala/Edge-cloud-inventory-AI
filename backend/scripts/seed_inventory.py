from pathlib import Path

import pandas as pd

from backend.app.database.session import SessionLocal
from backend.app.models.inventory import Inventory


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INVENTORY_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "inventory.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading inventory data...")

df = pd.read_csv(
    INVENTORY_FILE
)

print(
    f"Inventory rows found: {len(df):,}"
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = {
    "store_id",
    "product_id",
    "current_stock",
    "safety_stock",
    "capacity",
}

missing_columns = (
    required_columns
    - set(df.columns)
)

if missing_columns:
    raise ValueError(
        "Missing inventory columns: "
        + str(missing_columns)
    )


# ============================================================
# DATABASE
# ============================================================

db = SessionLocal()

try:

    print()
    print("Importing inventory...")

    # Remove old inventory data so the script
    # can be safely rerun.
    db.query(Inventory).delete()

    db.commit()

    inventory_records = []

    for _, row in df.iterrows():

        inventory = Inventory(
            store_id=int(
                row["store_id"]
            ),
            product_id=int(
                row["product_id"]
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
        )

        inventory_records.append(
            inventory
        )

        # Insert in batches.
        if len(inventory_records) >= 500:

            db.add_all(
                inventory_records
            )

            db.commit()

            print(
                f"Imported "
                f"{len(inventory_records):,} rows..."
            )

            inventory_records = []

    # Remaining records
    if inventory_records:

        db.add_all(
            inventory_records
        )

        db.commit()

    # ========================================================
    # VERIFY
    # ========================================================

    count = (
        db.query(Inventory)
        .count()
    )

    print()
    print("=" * 60)
    print("INVENTORY IMPORT COMPLETE")
    print("=" * 60)

    print(
        f"Inventory rows in database: "
        f"{count:,}"
    )

except Exception:

    db.rollback()

    raise

finally:

    db.close()