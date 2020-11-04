import requests
from wsgiven import Application
from wsgiven.utils.wsgi import jsonify


def _handle_health_live(application):
    status = "200 OK"
    response_body, headers = jsonify({})

    if not application["workers"]:
        status = "422 Unprocessable Entity"
        response_body, headers = jsonify({"code": "NoWorkers", "description": "There are no any workers."})

    return status, response_body, headers


def health_live(application, environ, start_fn):  # noqa pylint: disable=unused-argument
    status, response_body, headers = _handle_health_live(application)

    start_fn(status, headers)
    return [response_body]


def health_ready(application, environ, start_fn):  # noqa pylint: disable=unused-argument
    status, response_body, headers = _handle_health_live(application)

    # FIXME: make sure _handle_health_live status more clear
    if status == "200 OK" and application["config"].get("application_health_ready_url"):
        application["client_session"] = application["client_session"] or requests.Session()

        resp = application["client_session"].get(application["config"]["application_health_ready_url"])

        if resp.status_code == 200:
            response_body, headers = jsonify(resp.json())
        else:
            status = "422 Unprocessable Entity"
            data = {
                "code": "ServiceNotReady",
                "description": "The few of service subsystems is not working to successfully complete the request.",
            }

            if resp.headers.get("Content-Type") == "application/json":
                data["fields"] = resp.json()
            else:
                data["non_field_errors"] = [resp.text]
            response_body, headers = jsonify(data)

    start_fn(status, headers)
    return [response_body]


def create_application(config=None):
    routes = {"/health/live": health_live, "/health/ready": health_ready}
    return Application(routes=routes, config=config)
