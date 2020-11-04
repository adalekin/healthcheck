import pytest
from wsgiref_fake.http.client import HTTPClient
from wsgiref_fake.server import make_server

from healthcheck.application import create_application


@pytest.fixture(scope="function")
def fx_application():
    app = create_application()
    app["workers"] = 1

    return app


@pytest.fixture(scope="function")
def fx_application_without_workers(fx_application):  # noqa pylint: disable=redefined-outer-name
    fx_application["workers"] = 0

    return fx_application


@pytest.fixture(scope="function")
def fx_server(fx_application):  # noqa pylint: disable=redefined-outer-name
    return make_server(app=fx_application)


@pytest.fixture(scope="function")
def fx_http_client(fx_server):  # noqa pylint: disable=redefined-outer-name
    return HTTPClient(server=fx_server)
