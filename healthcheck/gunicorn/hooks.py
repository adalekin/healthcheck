import psutil
from gunicorn.instrument.statsd import Statsd

__all__ = ["post_worker_init", "worker_abort", "worker_exit"]

WORKERS = {}


def _ensure_workers(app):
    global WORKERS  # noqa pylint: disable=global-statement

    WORKERS = {pid: worker for pid, worker in WORKERS.items() if psutil.pid_exists(pid)}

    statsd = Statsd(app.cfg)

    statsd.debug(
        "{0} workers".format(len(WORKERS)),
        extra={"metric": "gunicorn.workers", "value": len(WORKERS), "mtype": "gauge"},
    )


def _add_worker(worker):
    global WORKERS  # noqa pylint: disable=global-statement
    WORKERS[worker.pid] = worker

    _ensure_workers(worker.app)


def _remove_worker(worker):
    global WORKERS  # noqa pylint: disable=global-statement

    if worker.pid in WORKERS:
        del WORKERS[worker.pid]

    _ensure_workers(worker.app)


def post_worker_init(worker):
    _add_worker(worker)


def worker_abort(worker):
    _remove_worker(worker)


def worker_exit(server, worker):  # noqa pylint: disable=unused-argument
    _remove_worker(worker)
