import os
from pathlib import Path

from dotenv import load_dotenv

VERSION = '26.1119.1736'

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)


ENVIRONMENTS = ('development', 'testing', 'production')
ENVIRONMENT = os.getenv('ENVIRONMENT')
if ENVIRONMENT not in ENVIRONMENTS:
    raise ValueError(f'Invalid ENVIRONMENT: {ENVIRONMENT}')


def _as_bool(value: str) -> bool:
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def _as_int(value: str) -> int:
    return int(value.strip())


LOG_DIR = Path(os.getenv('LOG_DIR', default=str(BASE_DIR / 'logs')))

# === Redis（broker 与 result backend 共用同一实例，靠 db 区分）===
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', REDIS_URL)

# === Worker ===
WORKER_CONCURRENCY = _as_int(os.getenv('WORKER_CONCURRENCY', '8'))
WORKER_PREFETCH_MULTIPLIER = _as_int(os.getenv('WORKER_PREFETCH_MULTIPLIER', '1'))

# === 任务与结果 ===
CELERY_TASK_IGNORE_RESULT = _as_bool(os.getenv('CELERY_TASK_IGNORE_RESULT', '0'))
RESULT_EXPIRES = _as_int(os.getenv('RESULT_EXPIRES', '86400'))

# Redis 中未 ack 的消息超过该秒数会被重新投递，必须大于最长任务耗时，否则会重复执行
BROKER_VISIBILITY_TIMEOUT = _as_int(os.getenv('BROKER_VISIBILITY_TIMEOUT', '7200'))

# 任务模块，worker 启动时导入以完成按名字注册
CELERY_INCLUDE = ('src.tasks.sleep',)
