from pathlib import Path

import pandas as pd

from edge.node import EdgeNode
from cloud.aggregator import CloudAggregator


BASE_DIR = Path(__file__).resolve().parents[1]

INVENTORY_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "inventory.csv"
)


def run_edge_cloud_simulation():

    print("Loading inventory data...")

    inventory = pd.read_csv(
        INVENTORY_PATH
    )

    cloud = CloudAggregator()

    print()
    print("=" * 60)
    print("EDGE → CLOUD SIMULATION")
    print("=" * 60)

    # ========================================================
    # EDGE PROCESSING
    # ========================================================

    for store_id, store_inventory in inventory.groupby(
        "store_id"
    ):

        node = EdgeNode(
            store_id=int(store_id)
        )

        records = (
            store_inventory
            .to_dict(orient="records")
        )

        edge_result = node.process_inventory(
            records
        )

        # Send processed information to cloud
        cloud.receive(
            edge_result
        )

        print(
            f"Store {store_id}: "
            f"{edge_result['low_stock_count']} low-stock, "
            f"{edge_result['critical_stock_count']} critical"
        )

    # ========================================================
    # CLOUD AGGREGATION
    # ========================================================

    cloud_result = cloud.aggregate()

    print()
    print("=" * 60)
    print("CLOUD AGGREGATION")
    print("=" * 60)

    print(
        f"Stores processed: "
        f"{cloud_result['stores_processed']}"
    )

    print(
        f"Products processed: "
        f"{cloud_result['total_products']}"
    )

    print(
        f"Total low-stock items: "
        f"{cloud_result['total_low_stock']}"
    )

    print(
        f"Total critical items: "
        f"{cloud_result['total_critical_stock']}"
    )

    # ========================================================
    # CLOUD PRIORITY ANALYSIS
    # ========================================================

    priority_stores = (
        cloud.get_priority_stores()
    )

    print()
    print("=" * 60)
    print("CLOUD PRIORITY ANALYSIS")
    print("=" * 60)

    for store in priority_stores[:10]:

        print(
            f"Store {store['store_id']}: "
            f"{store['low_stock_count']} low-stock, "
            f"{store['critical_stock_count']} critical, "
            f"Priority={store['priority']}"
        )

    return cloud_result


if __name__ == "__main__":

    run_edge_cloud_simulation()