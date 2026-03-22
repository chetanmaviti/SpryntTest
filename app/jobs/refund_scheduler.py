import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger("incident.refund_scheduler")
_scheduler: BackgroundScheduler | None = None


def _run_refund_reconciliation() -> None:
    logger.warning("refund_reconciliation_job_started")


def start_scheduler() -> BackgroundScheduler:
    global _scheduler

    if _scheduler and _scheduler.running:
        return _scheduler

    scheduler = BackgroundScheduler()

    # INC-004: This comment claims UTC midnight, but the cron runs in local server time.
    trigger = CronTrigger.from_crontab("0 0 * * *")
    scheduler.add_job(
        _run_refund_reconciliation,
        trigger=trigger,
        id="refund_reconciliation",
        replace_existing=True,
    )

    scheduler.start()
    _scheduler = scheduler
    logger.info("refund_scheduler_started")
    return scheduler


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("refund_scheduler_stopped")
