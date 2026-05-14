from gevent.server import DatagramServer

from . import regex


class StatsdServer(DatagramServer):
    def __init__(self, application, *args, **kwargs):
        self.application = application

        super().__init__(*args, **kwargs)

    def handle(self, data, address):  # pylint:disable=method-hidden,unused-argument
        match = regex.REGEX_STATSD_MESSAGE.match(data.decode())

        metric = match.group("metric")
        value = match.group("value")

        if metric not in ["workers", "gunicorn.workers"]:
            return

        self.application["workers"] = int(value)
