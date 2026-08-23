from pathlib import Path

import pandas as pd

from backend.app.database.session import SessionLocal
from backend.app.models.forecast import Forecast


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FORECAST_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecast_results.csv"
)


# ============================================================
# LOAD FORECAST DATA
# ============================================================

print("Loading forecast data...")

df = pd.read_csv(
    FORECAST_FILE
)

print(
    f"Forecast rows found: {len(df):,}"
)


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = {
    "date",
    "store_id",
    "product_id",
    "predicted_demand",
}

missing_columns = (
    required_columns
    - set(df.columns)
)

if missing_columns:

    raise ValueError(
        "Missing columns: "
        + str(missing_columns)
    )


# ============================================================
# CREATE DATABASE SESSION
# ============================================================

db = SessionLocal()


try:

    # --------------------------------------------------------
    # Clear existing forecasts
    # --------------------------------------------------------

    print(
        "Removing existing forecast records..."
    )

    db.query(Forecast).delete()

    db.commit()


    # --------------------------------------------------------
    # Insert forecasts
    # --------------------------------------------------------

    print(
        "Importing forecasts..."
    )

    forecasts = []

    for _, row in df.iterrows():

        forecast = Forecast(

            store_id=int(
                row["store_id"]
            ),

            product_id=int(
                row["product_id"]
            ),

            forecast_date=pd.to_datetime(
                row["date"]
            ).date(),

            predicted_demand=float(
                row["predicted_demand"]
            ),

            model_version=(
                "hist_gradient_boosting_v1"
            ),
        )

        forecasts.append(
            forecast
        )


        # ----------------------------------------------------
        # Insert in batches
        # ----------------------------------------------------

        if len(forecasts) >= 5000:

            db.add_all(
                forecasts
            )

            db.commit()

            print(
                f"Imported "
                f"{len(forecasts):,} rows..."
            )

            forecasts = []


    # --------------------------------------------------------
    # Remaining rows
    # --------------------------------------------------------

    if forecasts:

        db.add_all(
            forecasts
        )

        db.commit()


    # --------------------------------------------------------
    # Final count
    # --------------------------------------------------------

    count = (
        db.query(Forecast)
        .count()
    )

    print()
    print("=" * 60)
    print(
        "FORECAST IMPORT COMPLETE"
    )
    print("=" * 60)

    print(
        f"Database forecast rows: "
        f"{count:,}"
    )


except Exception:

    db.rollback()

    raise


finally:

    db.close()