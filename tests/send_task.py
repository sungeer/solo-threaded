"""模拟其他后端按任务名提交耗时任务。"""
import argparse
import os
import time

from celery import Celery

BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/1')
BACKEND_URL = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/2')

celery = Celery(broker=BROKER_URL, backend=BACKEND_URL)


def send(seconds: float, count: int) -> tuple[list, float]:
    started = time.monotonic()
    results = [
        celery.send_task('demo.sleep', kwargs={'seconds': seconds})
        for _ in range(count)
    ]
    data = [result.get(timeout=seconds * 2 + 30) for result in results]
    return data, round(time.monotonic() - started, 2)


def main():
    parser = argparse.ArgumentParser(description='按任务名提交 demo.sleep')
    parser.add_argument('--seconds', type=float, default=5.0, help='每个任务耗时秒数')
    parser.add_argument('--count', type=int, default=1, help='并发提交数量')
    args = parser.parse_args()

    data, elapsed = send(args.seconds, args.count)
    print(data)
    print(f'wall={elapsed}s')


if __name__ == '__main__':
    main()
