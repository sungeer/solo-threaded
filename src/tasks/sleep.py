import time

from celery.utils.log import get_task_logger

from src.main import app

logger = get_task_logger(__name__)


@app.task(name='demo.sleep')
def sleep_task(seconds: float = 10) -> dict:
    logger.info('sleep_task start: seconds=%s', seconds)

    started = time.monotonic()

    time.sleep(seconds)

    elapsed = round(time.monotonic() - started, 3)

    logger.info('sleep_task done: elapsed=%s', elapsed)

    return {'seconds': seconds, 'elapsed': elapsed}
