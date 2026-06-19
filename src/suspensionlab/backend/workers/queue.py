import os
from redis import Redis
from rq import Queue

_redis_conn = None
_job_queue = None

def _get_redis_conn():
    global _redis_conn
    if _redis_conn is None:
        redis_url = os.getenv("REDIS_URL", "")
        if not redis_url:
            raise RuntimeError("REDIS_URL is not set — Redis-backed features unavailable.")
        _redis_conn = Redis.from_url(redis_url)
    return _redis_conn

def _get_job_queue():
    global _job_queue
    if _job_queue is None:
        _job_queue = Queue("default", connection=_get_redis_conn())
    return _job_queue

# Proxy objects so existing code that does `from queue import job_queue` still works
class _LazyQueue:
    def __getattr__(self, name):
        return getattr(_get_job_queue(), name)
    def enqueue(self, *args, **kwargs):
        return _get_job_queue().enqueue(*args, **kwargs)

class _LazyRedis:
    @property
    def connection(self):
        return _get_redis_conn()
    def __getattr__(self, name):
        return getattr(_get_redis_conn(), name)

job_queue = _LazyQueue()
