from pathlib import Path

import pandas as pd

from backend.app.database.session import SessionLocal
from backend.app.models.validated_action import ValidatedAction


BASE_DIR = Path(__file__).resolve().parents[2]

VALIDATED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "validated_action_plan.csv"
)


print("Loading validated action data...")

df = pd.read_csv(VALIDATED_FILE)

print(
    f"Validated action rows found: {len(df):,}"
)


required_columns = {
    "store_id",
    "product_id",
    "action",
    "quantity",
    "from_store_id",
    "priority",
    "reason",
    "current_stock",
    "safety_stock",
    "capacity",
    "forecast_demand",
    "validation_status",
    "validation_reason",
    "required_stock",
    "stock_after_transfer",
    "remaining_shortage",
}


missing_columns = (
    required_columns - set(df.columns)
)

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


db = SessionLocal()

try:

    print()
    print("Removing existing validated actions...")

    db.query(ValidatedAction).delete()
    db.commit()

    print("Importing validated actions...")

    records = []

    for _, row in df.iterrows():

        from_store_id = None

        if pd.notna(row["from_store_id"]):
            from_store_id = int(
                row["from_store_id"]
            )

        record = ValidatedAction(
            store_id=int(row["store_id"]),
            product_id=int(row["product_id"]),
            action=str(row["action"]),
            quantity=int(row["quantity"]),
            from_store_id=from_store_id,
            priority=str(row["priority"]),
            reason=str(row["reason"]),
            current_stock=int(row["current_stock"]),
            safety_stock=int(row["safety_stock"]),
            capacity=int(row["capacity"]),
            forecast_demand=float(
                row["forecast_demand"]
            ),
            validation_status=str(
                row["validation_status"]
            ),
            validation_reason=str(
                row["validation_reason"]
            ),
            required_stock=float(
                row["required_stock"]
            ),
            stock_after_transfer=float(
                row["stock_after_transfer"]
            ),
            remaining_shortage=float(
                row["remaining_shortage"]
            ),
        )

        records.append(record)

        if len(records) >= 100:

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


    count = (
        db.query(ValidatedAction)
        .count()
    )


    print()
    print("=" * 60)
    print("VALIDATED ACTION IMPORT COMPLETE")
    print("=" * 60)

    print(
        f"Database validated actions: {count:,}"
    )

except Exception:

    db.rollback()
    raise

finally:

    db.close()