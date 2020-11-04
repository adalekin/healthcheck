# Healthcheck

`Healthcheck` provides liveness and readiness probes over HTTP. It uses the statsD protocol over
UDP to receive metrics and provides liveness and readiness HTTP endpoints.

## Usage

First of all you need to run `Healthcheck` web application:

```sh
python -m healthcheck --host 0.0.0.0 --port 8001
```

After that you have the following integration options:

### Gevent

TODO

### Gunicorn

Add [Gunicorn](https://gunicorn.org/) hooks to your `gunicorn.conf.py`:

```python
from healthcheck.gunicorn.hooks import *

# gunicorn.conf.py goes here
# ...
```

## Command line arguments

```
usage: __main__.py [-h] [-H HOST] [-P PORT] [--statsd-host STATSD_HOST]
                   [--statsd-port STATSD_PORT] [-v]
                   [--application-health-ready-url URL]

A simple "sidecar" healthcheck application. It uses the statsD protocol over
UDP to receive metrics and provides liveness and readiness HTTP endpoints.

optional arguments:
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

  **Liveness Probe**. Is designed to know when the application is running.

  Status Codes:
  - **200** OK
  - **422** The service is not down

    **Response JSON Object:**
    - code (string). The error code.
      - NoWorkers. There are no any workers.
    - description (string). The error description.

- `GET /health/ready`

  **Readiness Probe**. Is designed to know when the application is ready to serve the request.

  `Healthcheck` makes a request on `--application-health-ready-url` to get a detailed application readiness state in the current configuration.

  Status Codes:
  - **200** OK
  - **422** The service is not ready to serve the client requests

    **Response JSON Object:**
    - The service name.
    - The service current status.
