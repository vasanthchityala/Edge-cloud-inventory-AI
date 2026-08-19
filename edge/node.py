from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class EdgeNode:
    """
    Simulates an inventory edge node for one store.

    The edge node performs lightweight local processing
    before sending relevant information to the cloud.
    """

    store_id: int

    def process_inventory(
        self,
        inventory_records: list[dict],
    ) -> Dict[str, Any]:

        total_products = len(inventory_records)

        low_stock = []
        critical_stock = []

        for item in inventory_records:

            current_stock = item["current_stock"]
            safety_stock = item["safety_stock"]

            if current_stock <= 0:

                critical_stock.append(item)

            elif current_stock < safety_stock:

                low_stock.append(item)

        return {
            "store_id": self.store_id,
            "total_products": total_products,
            "low_stock_count": len(low_stock),
            "critical_stock_count": len(critical_stock),
            "low_stock_items": low_stock,
            "critical_stock_items": critical_stock,
        }