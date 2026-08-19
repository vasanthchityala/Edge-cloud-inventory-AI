from pathlib import Path
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

NUM_STORES = 20
NUM_PRODUCTS = 100

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

rng = np.random.default_rng(SEED)

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. STORES
# ============================================================

store_ids = np.arange(1, NUM_STORES + 1)

cities = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Delhi",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Kochi",
]

store_sizes = rng.choice(
    ["small", "medium", "large"],
    size=NUM_STORES,
    p=[0.3, 0.5, 0.2],
)

store_capacity = {
    "small": 300,
    "medium": 700,
    "large": 1500,
}

stores = pd.DataFrame({
    "store_id": store_ids,
    "store_name": [f"Store_{i:03d}" for i in store_ids],
    "city": rng.choice(cities, NUM_STORES),
    "store_size": store_sizes,
})

stores["capacity"] = stores["store_size"].map(store_capacity)

stores.to_csv(
    RAW_DIR / "stores.csv",
    index=False,
)


# ============================================================
# 2. PRODUCTS
# ============================================================

product_ids = np.arange(1, NUM_PRODUCTS + 1)

categories = [
    "Electronics",
    "Home Appliances",
    "Groceries",
    "Personal Care",
    "Fashion",
    "Sports",
    "Stationery",
    "Accessories",
]

product_categories = rng.choice(
    categories,
    NUM_PRODUCTS,
)

products = pd.DataFrame({
    "product_id": product_ids,
    "sku": [f"SKU-{i:05d}" for i in product_ids],
    "product_name": [f"Product_{i:04d}" for i in product_ids],
    "category": product_categories,
})

products["base_price"] = np.round(
    rng.uniform(100, 50000, NUM_PRODUCTS),
    2,
)

products["base_demand"] = rng.uniform(
    5,
    40,
    NUM_PRODUCTS,
)

products.to_csv(
    RAW_DIR / "products.csv",
    index=False,
)


# ============================================================
# 3. DATE DIMENSION
# ============================================================

dates = pd.date_range(
    START_DATE,
    END_DATE,
    freq="D",
)

date_df = pd.DataFrame({
    "date": dates,
})

date_df["day_of_week"] = date_df["date"].dt.dayofweek
date_df["month"] = date_df["date"].dt.month
date_df["week_of_year"] = date_df["date"].dt.isocalendar().week.astype(int)
date_df["year"] = date_df["date"].dt.year

date_df["is_weekend"] = (
    date_df["day_of_week"] >= 5
).astype(int)

# Indian-style major holiday periods for synthetic business data
date_df["is_holiday"] = (
    (
        (date_df["month"] == 10)
        & (date_df["date"].dt.day.between(20, 31))
    )
    |
    (
        (date_df["month"] == 11)
        & (date_df["date"].dt.day.between(1, 15))
    )
).astype(int)


# ============================================================
# 4. SALES DATA
# ============================================================

sales_chunks = []

for store_id in store_ids:

    store_multiplier = rng.uniform(0.7, 1.5)

    for product_index, product_id in enumerate(product_ids):

        dates_count = len(dates)

        base_demand = products.loc[
            product_index,
            "base_demand",
        ]

        category = products.loc[
            product_index,
            "category",
        ]

        # Category demand multiplier
        category_multiplier = {
            "Electronics": 1.2,
            "Home Appliances": 0.9,
            "Groceries": 1.5,
            "Personal Care": 1.1,
            "Fashion": 1.3,
            "Sports": 0.8,
            "Stationery": 0.7,
            "Accessories": 1.0,
        }[category]

        # Weekly seasonality
        weekend_multiplier = np.where(
            date_df["is_weekend"].values == 1,
            1.20,
            1.00,
        )

        # Holiday demand increase
        holiday_multiplier = np.where(
            date_df["is_holiday"].values == 1,
            1.45,
            1.00,
        )

        # Yearly trend
        trend = np.linspace(
            1.0,
            1.15,
            dates_count,
        )

        # Random demand variation
        noise = rng.normal(
            1.0,
            0.15,
            dates_count,
        )

        noise = np.clip(
            noise,
            0.5,
            1.6,
        )

        # Promotion
        promotion = (
            rng.random(dates_count) < 0.12
        ).astype(int)

        promotion_multiplier = np.where(
            promotion == 1,
            1.35,
            1.0,
        )

        # Price variation
        base_price = products.loc[
            product_index,
            "base_price",
        ]

        price = base_price * rng.uniform(
            0.90,
            1.10,
            dates_count,
        )

        # Final demand
        expected_demand = (
            base_demand
            * store_multiplier
            * category_multiplier
            * weekend_multiplier
            * holiday_multiplier
            * trend
            * promotion_multiplier
            * noise
        )

        quantity = rng.poisson(
            np.maximum(
                expected_demand,
                0.1,
            )
        )

        chunk = pd.DataFrame({
            "date": dates,
            "store_id": store_id,
            "product_id": product_id,
            "category": category,
            "price": np.round(price, 2),
            "promotion": promotion,
            "is_weekend": date_df["is_weekend"].values,
            "is_holiday": date_df["is_holiday"].values,
            "quantity": quantity,
        })

        sales_chunks.append(chunk)


sales = pd.concat(
    sales_chunks,
    ignore_index=True,
)

# Sort chronologically
sales = sales.sort_values(
    ["date", "store_id", "product_id"]
).reset_index(drop=True)


# ============================================================
# 5. SAVE SALES
# ============================================================

sales.to_csv(
    RAW_DIR / "sales.csv",
    index=False,
)


# ============================================================
# 6. INVENTORY SNAPSHOT
# ============================================================

inventory_rows = []

for store_id in store_ids:

    capacity = int(
        stores.loc[
            stores["store_id"] == store_id,
            "capacity",
        ].iloc[0]
    )

    for product_id in product_ids:

        current_stock = rng.integers(
            10,
            max(20, capacity // 2),
        )

        safety_stock = rng.integers(
            10,
            max(15, capacity // 5),
        )

        inventory_rows.append({
            "store_id": store_id,
            "product_id": product_id,
            "current_stock": int(current_stock),
            "safety_stock": int(safety_stock),
            "capacity": capacity,
            "lead_time_days": int(
                rng.integers(1, 8)
            ),
        })


inventory = pd.DataFrame(
    inventory_rows
)

inventory.to_csv(
    RAW_DIR / "inventory.csv",
    index=False,
)


# ============================================================
# 7. SUMMARY
# ============================================================

print()
print("=" * 60)
print("DATASET GENERATION COMPLETE")
print("=" * 60)

print(f"Stores:        {len(stores):,}")
print(f"Products:      {len(products):,}")
print(f"Sales rows:    {len(sales):,}")
print(f"Inventory rows:{len(inventory):,}")

print()
print("Files created:")

print(RAW_DIR / "stores.csv")
print(RAW_DIR / "products.csv")
print(RAW_DIR / "sales.csv")
print(RAW_DIR / "inventory.csv")

print("=" * 60)