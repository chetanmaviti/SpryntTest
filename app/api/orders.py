import logging
import traceback
import uuid

from fastapi import APIRouter, HTTPException

from app.db.fake_pool import FakeConnection, FakePool
from app.models import OrderRequest, OrderResponse
from app.services.dedupe_cache import cache_size, remember, seen_recently
from app.services.inventory_client import reserve_inventory
from app.services.payment_client import charge_payment

router = APIRouter(tags=["orders"])
logger = logging.getLogger("incident.orders")
pool = FakePool()


@router.post("/orders", response_model=OrderResponse)
def create_order(order: OrderRequest) -> OrderResponse:
    request_id = f"req_{uuid.uuid4().hex[:12]}"
    payload = order.model_dump(by_alias=True)

    logger.info(
        "order_received request_id=%s order_id=%s amount=%.2f sku=%s",
        request_id,
        order.order_id,
        order.amount,
        order.sku,
    )

    if seen_recently(order.order_id):
        logger.info(
            "duplicate_order request_id=%s order_id=%s cache_size=%s",
            request_id,
            order.order_id,
            cache_size(),
        )
        return OrderResponse(
            status="duplicate",
            requestId=request_id,
            message="Order already seen recently",
        )

    remember(order.order_id)

    conn: FakeConnection | None = None
    leak_connection = False

    try:
        conn = pool.acquire()

        if order.amount > 5000:
            raise ValueError("high risk transaction requires manual review")

        reserve_inventory(payload)
        charge_payment(payload)
        conn.execute("INSERT INTO orders (order_id, user_id, amount, sku) VALUES (...)" )

        logger.info(
            "order_placed request_id=%s order_id=%s pool_active=%s",
            request_id,
            order.order_id,
            pool.active_connections(),
        )
        return OrderResponse(
            status="accepted",
            requestId=request_id,
            message="Order accepted",
        )

    except ValueError:
        # INC-006: missing correlation id and logs full payload with stack trace.
        logger.error("payload_dump=%s", payload)
        logger.error("stack=%s", traceback.format_exc())
        logger.exception("order_processing_failed_without_correlation")

        # INC-003: one exception path leaks DB connection by skipping release.
        leak_connection = True
        raise HTTPException(status_code=500, detail="order processing failed")

    except Exception as exc:
        logger.exception(
            "order_processing_failed request_id=%s order_id=%s error=%s",
            request_id,
            order.order_id,
            exc,
        )
        raise HTTPException(status_code=502, detail="downstream dependency error") from exc

    finally:
        if conn is not None and not leak_connection:
            pool.release(conn)
