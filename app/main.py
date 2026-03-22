import logging
from pathlib import Path

from fastapi import FastAPI

from app.api.orders import router as orders_router
from app.jobs.refund_scheduler import start_scheduler, stop_scheduler

APP_NAME = "checkout-ops-demo-py"
LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "incident.log"


def configure_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)


configure_logging()
app = FastAPI(title=APP_NAME)
app.include_router(orders_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.on_event("startup")
def on_startup() -> None:
    logging.getLogger("incident.main").info("app_startup")
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown() -> None:
    logging.getLogger("incident.main").info("app_shutdown")
    stop_scheduler()
