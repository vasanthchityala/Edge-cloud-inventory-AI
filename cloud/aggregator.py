from collections import defaultdict
from typing import Any


class CloudAggregator:
    """
    Simulates the cloud layer that receives
    processed information from multiple edge nodes.
    """

    def __init__(self):
        self.store_data = {}

    def receive(self, edge_result: dict[str, Any]) -> None:
        store_id = edge_result["store_id"]

        self.store_data[store_id] = edge_result

    def aggregate(self) -> dict[str, Any]:

        total_products = 0
        total_low_stock = 0
        total_critical_stock = 0

        critical_by_store = defaultdict(list)

        for store_id, data in self.store_data.items():

            total_products += data["total_products"]

            total_low_stock += (
                data["low_stock_count"]
            )

            total_critical_stock += (
                data["critical_stock_count"]
            )

            critical_by_store[store_id] = (
                data["critical_stock_items"]
            )

        return {
            "stores_processed": len(
                self.store_data
            ),
            "total_products": total_products,
            "total_low_stock": total_low_stock,
            "total_critical_stock": total_critical_stock,
            "critical_by_store": dict(
                critical_by_store
            ),
        }

    def get_priority_stores(self) -> list[dict]:

        priority_stores = []

        for store_id, data in self.store_data.items():

            low_stock = data["low_stock_count"]
            critical_stock = data["critical_stock_count"]

            if critical_stock > 0:

                priority = "CRITICAL"

            elif low_stock >= 20:

                priority = "HIGH"

            elif low_stock >= 10:

                priority = "MEDIUM"

            else:

                priority = "LOW"

            priority_stores.append({
                "store_id": store_id,
                "low_stock_count": low_stock,
                "critical_stock_count": critical_stock,
                "priority": priority,
            })

        return sorted(
            priority_stores,
            key=lambda x: (
                x["critical_stock_count"],
                x["low_stock_count"],
            ),
            reverse=True,
        )