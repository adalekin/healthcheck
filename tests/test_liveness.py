def test_liveness_no_workers(fx_application_without_workers, fx_http_client):
    response = fx_http_client.request(method="GET", path="/health/live")
    assert response.status == 422


def test_liveness(fx_http_client):
    response = fx_http_client.request(method="GET", path="/health/live")
    assert response.status == 200
