from pathlib import Path
from datetime import datetime

import pandas as pd

from backend.app.database.session import SessionLocal
from backend.app.models.transfer import Transfer


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

TRANSFER_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "optimized_transfers.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading optimized transfer data...")

df = pd.read_csv(TRANSFER_FILE)

print(
    f"Transfer rows found: {len(df):,}"
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = {
    "product_id",
    "from_store_id",
    "to_store_id",
    "transfer_quantity",
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
    print("Removing existing recommended transfers...")

    db.query(Transfer).filter(
        Transfer.status == "recommended"
    ).delete(
        synchronize_session=False
    )

    db.commit()

    print("Importing optimized transfers...")

    records = []

    for _, row in df.iterrows():

        from_store_id = int(
            row["from_store_id"]
        )

        to_store_id = int(
            row["to_store_id"]
        )

        product_id = int(
            row["product_id"]
        )

        quantity = int(
            row["transfer_quantity"]
        )

        if quantity <= 0:
            continue

        if from_store_id == to_store_id:
            continue

        transfer = Transfer(
            from_store_id=from_store_id,
            to_store_id=to_store_id,
            product_id=product_id,
            quantity=quantity,
            status="recommended",
            created_at=datetime.utcnow(),
        )

        records.append(transfer)

        if len(records) >= 100:

            db.add_all(records)

            db.commit()

            print(
                f"Imported {len(records):,} transfers..."
            )

            records = []

    if records:

        db.add_all(records)

        db.commit()

        print(
            f"Imported {len(records):,} transfers..."
        )


    # ========================================================
    # VERIFY
    # ========================================================

    count = (
        db.query(Transfer)
        .filter(
            Transfer.status == "recommended"
        )
        .count()
    )

    print()
    print("=" * 60)
    print("TRANSFER IMPORT COMPLETE")
    print("=" * 60)

    print(
        f"Recommended transfers in database: {count:,}"
    )

except Exception:

    db.rollback()

    raise

finally:

    db.close()