from typing import Dict

# INC-002: Global cache that never evicts old IDs.
_SEEN_ORDERS: Dict[str, bool] = {}


def remember(order_id: str) -> None:
    _SEEN_ORDERS[order_id] = True


def seen_recently(order_id: str) -> bool:
    return _SEEN_ORDERS.get(order_id, False)


def cache_size() -> int:
    return len(_SEEN_ORDERS)
