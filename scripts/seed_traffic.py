import argparse
import json
import random
import time
from typing import Any, Dict

import requests

BASE_URL = "http://127.0.0.1:8000"


def post_order(payload: Dict[str, Any], base_url: str) -> tuple[int, str]:
    response = requests.post(f"{base_url}/orders", json=payload, timeout=2)
    return response.status_code, response.text


def build_payload(i: int) -> Dict[str, Any]:
    # Duplicate IDs and high-value orders amplify cache growth and leak paths.
    if i % 7 == 0:
        return {
            "orderId": f"ord_hot_{i % 3}",
            "userId": f"usr_{i % 10}",
            "amount": 149.99,
            "sku": "SKU-RED-TSHIRT",
        }

    if i % 9 == 0:
        return {
            "orderId": f"ord_risky_{i}",
            "userId": f"usr_{i % 10}",
            "amount": 7000.00,
            "sku": "SKU-GOLD-BUNDLE",
        }

    return {
        "orderId": f"ord_{10000 + i}",
        "userId": f"usr_{i % 10}",
        "amount": round(random.uniform(20, 350), 2),
        "sku": random.choice(["SKU-RED-TSHIRT", "SKU-BLUE-HOODIE", "SKU-WHITE-CAP"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate demo traffic for checkout-ops-demo-py")
    parser.add_argument("--count", type=int, default=120, help="number of orders to send")
    parser.add_argument("--base-url", default=BASE_URL, help="base URL for the API")
    parser.add_argument(
        "--sleep-max",
        type=float,
        default=0.12,
        help="max random sleep between requests in seconds",
    )
    args = parser.parse_args()

    status_counts: Dict[int, int] = {}
    failures = 0

    for i in range(args.count):
        payload = build_payload(i)
        print(json.dumps(payload))
        try:
            status, body = post_order(payload, args.base_url)
            status_counts[status] = status_counts.get(status, 0) + 1
            print(status, body)
        except Exception as exc:
            failures += 1
            print(f"request failed: {exc}")
        if args.sleep_max > 0:
            time.sleep(random.uniform(0.0, args.sleep_max))

    print("summary", {"statuses": status_counts, "transportFailures": failures})


if __name__ == "__main__":
    main()
