# hermitess

Celery worker：单进程多线程（threads pool）消费耗时任务，broker 与 result backend 都用 Redis。
任务只通过任务名字符串提交（`send_task('demo.sleep', ...)`），没有定时任务。

## 安装

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

配置见 `.env.example`（复制为 `.env`）。

## 启动 worker

```
celery -A src.main:app worker --pool=threads --concurrency=8 --loglevel=INFO
```

`--pool=threads` 与 `--concurrency` 会覆盖代码里的默认值，按机器规格调整即可。

## 提交任务

其他 Python 后端只需构造同样的 Celery 客户端：

```python
from celery import Celery

celery = Celery(broker='redis://127.0.0.1:6379/1', backend='redis://127.0.0.1:6379/2')

result = celery.send_task('demo.sleep', kwargs={'seconds': 30})
print(result.get(timeout=60))
```

内置示例任务（一个任务一个模块，只做 IO 耗时）：

| 任务名 | 模块 | 参数 | 说明 |
| --- | --- | --- | --- |
| `demo.sleep` | `src/tasks/sleep.py` | `seconds` | 阻塞等待 |

## 注意

- threads pool 不支持 `time_limit` / `soft_time_limit`，任务无法被强制中断；
  需要超时就在任务内部用协作式检查。
- GIL 限制下线程池只对 IO 型任务有并行收益，纯 CPU 任务不会变快。
- 已开启 `task_acks_late=True`，worker 崩溃后任务会重新投递，任务必须幂等；
  `BROKER_VISIBILITY_TIMEOUT` 必须大于最长任务耗时，否则会重复执行。
- 任务结果默认保留 `RESULT_EXPIRES` 秒；不需要结果时设 `CELERY_TASK_IGNORE_RESULT=1`。

## 模拟提交

`tests/send_task.py` 模拟其他后端按任务名提交，可指定并发数量：

```
.venv/Scripts/python.exe tests/send_task.py --seconds 5 --count 2
```
