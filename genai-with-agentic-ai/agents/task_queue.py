"""
task_queue.py
Wrapper around RQ (Redis Queue) with a fallback to direct execution if Redis is unavailable.
"""
import logging

logger = logging.getLogger(__name__)

try:
    import redis
    from rq import Queue
    _redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    _queue = Queue(connection=_redis_conn)
    _HAS_REDIS = True
except Exception:
    _redis_conn = None
    _queue = None
    _HAS_REDIS = False
    logger.warning("Redis/RQ unavailable — falling back to direct execution of tasks")


def enqueue_task(task_type: str, payload: dict, priority: int = 50):
    """Enqueue a task. If Redis is unavailable, attempt direct execution.

    Returns a dict with enqueue metadata or direct execution result.
    """
    if _HAS_REDIS and _queue:
        try:
            job = _queue.enqueue('agents.workers.scraper_worker.handle_task', task_type, payload)
            logger.info(f"Enqueued task {task_type} to RQ (job id: {job.id})")
            return {"queued": True, "job_id": job.id}
        except Exception as e:
            logger.warning(f"Failed to enqueue task to RQ: {e}")

    # Fallback: direct execution
    try:
        from agents.workers.scraper_worker import handle_task
        result = handle_task(task_type, payload)
        return {"queued": False, "executed": True, "result": result}
    except Exception as e:
        logger.error(f"Failed executing task directly: {e}")
        return {"queued": False, "executed": False, "error": str(e)}
