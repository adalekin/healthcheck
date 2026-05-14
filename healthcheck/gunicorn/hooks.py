import psutil
from gunicorn.instrument.statsd import Statsd

__all__ = ["post_worker_init", "worker_abort", "worker_exit"]

WORKERS = {}


def _ensure_workers(app):
    global WORKERS

    WORKERS = {pid: worker for pid, worker in WORKERS.items() if psutil.pid_exists(pid)}

    statsd = Statsd(app.cfg)

    statsd.debug(
        f"{len(WORKERS)} workers",
        extra={"metric": "gunicorn.workers", "value": len(WORKERS), "mtype": "gauge"},
    )


def _add_worker(worker):
    global WORKERS
    WORKERS[worker.pid] = worker

    _ensure_workers(worker.app)


def _remove_worker(worker):
    global WORKERS

    if worker.pid in WORKERS:
        del WORKERS[worker.pid]

    _ensure_workers(worker.app)


def post_worker_init(worker):
    _add_worker(worker)


def worker_abort(worker):
    _remove_worker(worker)


def worker_exit(_server, worker):
    _remove_worker(worker)
