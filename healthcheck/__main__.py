from gevent import monkey

monkey.patch_all()

# pylint: disable=wrong-import-position,wrong-import-order,ungrouped-imports
import argparse
import logging

from gevent.pywsgi import WSGIServer
from gevent_toolbelt.service import ServiceGroup
from gevent_toolbelt.signals import install_signal_handler

from .application import create_application
from .statsd import StatsdServer


def main():
    parser = argparse.ArgumentParser(
        description='A simple "sidecar" healthcheck application. '
        "It uses the statsD protocol over UDP to receive metrics and provides liveness and readiness HTTP endpoints."
    )
    parser.add_argument(
        "-H",
        "--host",
        metavar="HOST",
        default="localhost",
        help="The host that the server should bind on (default: %(default)s).",
    )
    parser.add_argument(
        "-P",
        "--port",
        metavar="PORT",
        default=8000,
        type=int,
        help="The port that the server should bind on (default: %(default)s).",
    )
    parser.add_argument(
        "--statsd-host",
        metavar="STATSD_HOST",
        default="localhost",
        help="The host of the statsd server (default: %(default)s).",
    )
    parser.add_argument(
        "--statsd-port",
        metavar="STATSD_PORT",
        default=8125,
        type=int,
        help="The port of the statsd server (default: %(default)s).",
    )
    parser.add_argument(
        "--application-health-ready-url",
        metavar="URL",
        help="The application URL which provides a readiness status (optional).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose_count",
        action="count",
        default=0,
        help="Activate verbose output to the console and specify the level of detail.",
    )

    args = parser.parse_args()

    logging.basicConfig(level=max(3 - args.verbose_count, 0) * 10, format="%(asctime)s %(levelname)s %(message)s")

    application = create_application(vars(args))
    service_group = ServiceGroup(
        [
            WSGIServer((args.host, args.port), application),
            StatsdServer(application, (args.statsd_host, args.statsd_port)),
        ]
    )

    install_signal_handler(service_group.stop)

    service_group.serve_forever()


if __name__ == "__main__":
    main()
