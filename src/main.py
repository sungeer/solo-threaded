from celery import Celery

from src import settings


def create_app() -> Celery:
    celery = Celery(
        'solo-threaded',
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=list(settings.CELERY_INCLUDE),
    )

    celery.conf.update(
        # 其他后端只通过任务名字符串提交，统一 JSON 序列化
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        # 结果保留在 Redis，按需关闭可省内存
        task_ignore_result=settings.CELERY_TASK_IGNORE_RESULT,
        result_expires=settings.RESULT_EXPIRES,
        task_track_started=True,
        # 执行完才 ack：worker 崩溃时任务会被重新投递，任务需幂等
        task_acks_late=True,
        worker_prefetch_multiplier=settings.WORKER_PREFETCH_MULTIPLIER,
        broker_transport_options={
            'visibility_timeout': settings.BROKER_VISIBILITY_TIMEOUT,
        },
        broker_connection_retry_on_startup=True,
        # 单进程多线程
        worker_pool='threads',
        worker_concurrency=settings.WORKER_CONCURRENCY,
    )

    return celery


app = create_app()
