import json


def test_readiness_no_workers(fx_application_without_workers, fx_http_client):  # noqa pylint: disable=unused-argument
    response = fx_http_client.request(method="GET", path="/health/ready")
    assert response.status == 422


def test_readiness_no_application_health_ready_url(fx_http_client):
    response = fx_http_client.request(method="GET", path="/health/ready")
    assert response.status == 200


def test_readiness(fx_application, fx_http_client, requests_mock):
    fx_application["config"]["application_health_ready_url"] = "http://example.com"

    requests_mock.get(
        fx_application["config"]["application_health_ready_url"],
        json={"db": "ok"},
        headers={"Content-Type": "application/json"},
        status_code=200,
    )

    response = fx_http_client.request(method="GET", path="/health/ready")
    assert response.status == 200
    assert json.loads(response.read().decode()) == {"db": "ok"}


def test_readiness_failed(fx_application, fx_http_client, requests_mock):
    fx_application["config"]["application_health_ready_url"] = "http://example.com"

    requests_mock.get(
        fx_application["config"]["application_health_ready_url"],
        json={"db": "error"},
        headers={"Content-Type": "application/json"},
        status_code=500,
    )

    response = fx_http_client.request(method="GET", path="/health/ready")
    assert response.status == 422
    assert json.loads(response.read().decode()) == {
        "code": "ServiceNotReady",
        "description": "The few of service subsystems is not working to successfully " "complete the request.",
        "fields": {"db": "error"},
    }
