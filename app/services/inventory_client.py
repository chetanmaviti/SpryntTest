from typing import Any, Dict

import requests

INVENTORY_URL = "http://127.0.0.1:9002/inventory/reserve"


def reserve_inventory(payload: Dict[str, Any]) -> Dict[str, Any]:
    """INC-005: Fail fast with no retries, fallback, or circuit breaker."""
    try:
        response = requests.post(INVENTORY_URL, json=payload, timeout=1.5)
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"status": "reserved"}
    except requests.RequestException as exc:
        raise RuntimeError("inventory reservation failed") from exc
