from typing import Any, Dict

import requests

PAYMENT_URL = "http://127.0.0.1:9001/payments/charge"


def charge_payment(payload: Dict[str, Any]) -> Dict[str, Any]:
    """INC-001: Payment call intentionally has no timeout and no retries."""
    try:
        response = requests.post(PAYMENT_URL, json=payload)
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"status": "charged"}
    except requests.RequestException as exc:
        raise RuntimeError("payment call failed") from exc
