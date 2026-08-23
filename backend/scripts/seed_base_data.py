from pathlib import Path
from decimal import Decimal

import pandas as pd

from backend.app.database.session import SessionLocal
from backend.app.models.product import Product
from backend.app.models.store import Store


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PRODUCTS_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "products.csv"
)

STORES_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "stores.csv"
)


# ============================================================
# LOAD CSV FILES
# ============================================================

print("Loading base data...")

products_df = pd.read_csv(
    PRODUCTS_FILE
)

stores_df = pd.read_csv(
    STORES_FILE
)

print(
    f"Products found: {len(products_df):,}"
)

print(
    f"Stores found: {len(stores_df):,}"
)


# ============================================================
# VALIDATE PRODUCT COLUMNS
# ============================================================

required_product_columns = {
    "product_id",
    "sku",
    "product_name",
    "category",
    "base_price",
}

missing_product_columns = (
    required_product_columns
    - set(products_df.columns)
)

if missing_product_columns:
    raise ValueError(
        "Missing product columns: "
        + str(missing_product_columns)
    )


# ============================================================
# VALIDATE STORE COLUMNS
# ============================================================

required_store_columns = {
    "store_id",
    "store_name",
    "city",
}

missing_store_columns = (
    required_store_columns
    - set(stores_df.columns)
)

if missing_store_columns:
    raise ValueError(
        "Missing store columns: "
        + str(missing_store_columns)
    )


# ============================================================
# DATABASE SESSION
# ============================================================

db = SessionLocal()


try:

    # ========================================================
    # PRODUCTS
    # ========================================================

    print()
    print("Importing products...")

    for _, row in products_df.iterrows():

        product = db.get(
            Product,
            int(row["product_id"]),
        )

        if product is None:

            product = Product(
                id=int(
                    row["product_id"]
                ),
                sku=str(
                    row["sku"]
                ),
                name=str(
                    row["product_name"]
                ),
                category=str(
                    row["category"]
                ),
                unit_price=Decimal(
                    str(row["base_price"])
                ),
            )

            db.add(product)

        else:

            product.sku = str(
                row["sku"]
            )

            product.name = str(
                row["product_name"]
            )

            product.category = str(
                row["category"]
            )

            product.unit_price = Decimal(
                str(row["base_price"])
            )


    db.commit()

    print(
        f"Products imported: "
        f"{db.query(Product).count():,}"
    )


    # ========================================================
    # STORES
    # ========================================================

    print()
    print("Importing stores...")

    for _, row in stores_df.iterrows():

        store = db.get(
            Store,
            int(row["store_id"]),
        )

        if store is None:

            store = Store(
                id=int(
                    row["store_id"]
                ),
                name=str(
                    row["store_name"]
                ),
                location=str(
                    row["city"]
                ),
            )

            db.add(store)

        else:

            store.name = str(
                row["store_name"]
            )

            store.location = str(
                row["city"]
            )


    db.commit()

    print(
        f"Stores imported: "
        f"{db.query(Store).count():,}"
    )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 60)
    print("BASE DATA IMPORT COMPLETE")
    print("=" * 60)

    print(
        f"Products in database: "
        f"{db.query(Product).count():,}"
    )

    print(
        f"Stores in database: "
        f"{db.query(Store).count():,}"
    )


except Exception:

    db.rollback()

    raise


finally:

    db.close()