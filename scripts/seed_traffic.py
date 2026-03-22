import json
import random
import time
from typing import Any, Dict

import requests

BASE_URL = "http://127.0.0.1:8000"


def post_order(payload: Dict[str, Any]) -> None:
    response = requests.post(f"{BASE_URL}/orders", json=payload, timeout=2)
    print(response.status_code, response.text)


def main() -> None:
    samples = [
        {
            "orderId": "ord_1001",
            "userId": "usr_1",
            "amount": 149.99,
            "sku": "SKU-RED-TSHIRT",
        },
        {
            "orderId": "ord_1001",
            "userId": "usr_1",
            "amount": 149.99,
            "sku": "SKU-RED-TSHIRT",
        },
        {
            "orderId": "ord_9999",
            "userId": "usr_2",
            "amount": 7000.00,
            "sku": "SKU-GOLD-BUNDLE",
        },
    ]

    for payload in samples:
        print(json.dumps(payload))
        try:
            post_order(payload)
        except Exception as exc:
            print(f"request failed: {exc}")
        time.sleep(random.uniform(0.2, 0.6))


if __name__ == "__main__":
    main()
