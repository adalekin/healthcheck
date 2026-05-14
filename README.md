# Healthcheck

[![CI](https://github.com/adalekin/healthcheck/actions/workflows/ci.yml/badge.svg)](https://github.com/adalekin/healthcheck/actions/workflows/ci.yml)
[![PyPI publish](https://github.com/adalekin/healthcheck/actions/workflows/release.yml/badge.svg)](https://github.com/adalekin/healthcheck/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`Healthcheck` is a small sidecar-style process that exposes **liveness** and **readiness** HTTP endpoints. It listens for StatsD-style UDP gauges (for example `gunicorn.workers`) so the HTTP layer can reflect how many workers are alive.

## Requirements

- Python 3.12 or newer

## Install

From PyPI:

```sh
pip install approck-healthcheck
```

The importable Python package remains **`healthcheck`** (for example `python -m healthcheck`, `from healthcheck.application import create_application`).

From a git checkout with [uv](https://docs.astral.sh/uv/):

```sh
uv sync --locked
uv run healthcheck --help
```

## Run

```sh
uv run healthcheck --host 0.0.0.0 --port 8001
# or
python -m healthcheck --host 0.0.0.0 --port 8001
```

## Integrations

### Gevent

The `healthcheck` CLI starts a Gevent `WSGIServer` for `/health/*` and a UDP StatsD listener on the configured host and port. Your workers (or Gunicorn hooks) should emit gauge metrics named `workers` or `gunicorn.workers` so liveness reflects the worker count.

### Gunicorn

Add [Gunicorn](https://gunicorn.org/) hooks to your `gunicorn.conf.py`:

```python
from healthcheck.gunicorn.hooks import *

# gunicorn.conf.py goes here
# ...
```

## Command line

```
usage: healthcheck [-h] [-H HOST] [-P PORT] [--statsd-host STATSD_HOST]
                   [--statsd-port STATSD_PORT]
                   [--application-health-ready-url URL] [-v]

A simple "sidecar" healthcheck application. It uses the statsD protocol over
UDP to receive metrics and provides liveness and readiness HTTP endpoints.

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  The host that the server should bind on (default:
                        localhost).
  -P PORT, --port PORT  The port that the server should bind on (default:
                        8000).
  --statsd-host STATSD_HOST
                        The host of the statsd server (default: localhost).
  --statsd-port STATSD_PORT
                        The port of the statsd server (default: 8125).
  --application-health-ready-url URL
                        The application URL which provides a readiness status
                        (optional).
  -v, --verbose         Activate verbose output to the console and specify the
                        level of detail.
```

## REST API

- `GET /health/live`

  **Liveness probe** — indicates whether the process considers workers available.

  Status codes:
  - **200** — workers gauge is positive.
  - **422** — no workers reported (`NoWorkers`).

  Error JSON:
  - `code` (string), e.g. `NoWorkers`.
  - `description` (string).

- `GET /health/ready`

  **Readiness probe** — same worker gate as liveness; if `--application-health-ready-url` is set, the handler proxies JSON from that URL or returns `ServiceNotReady` on non-200 responses.

  Status codes:
  - **200** — ready (including proxied JSON from the application URL when configured).
  - **422** — not ready.

## Development

Clone the repository, then install dependencies (uses the committed `uv.lock`) and run checks:

```bash
uv sync --locked
uv run ruff check healthcheck tests
uv run ruff format --check healthcheck tests
uv run pytest
```

To refresh dev dependencies and regenerate the lockfile:

```bash
uv lock --upgrade
```

To apply Ruff formatting (instead of only checking):

```bash
uv run ruff format healthcheck tests
```

## Contributing

Issues and **pull requests** (including from forks) are welcome. Please run `uv run ruff check`, `uv run ruff format --check`, and `uv run pytest` before submitting a change.

## License

MIT — see [LICENSE](LICENSE).
