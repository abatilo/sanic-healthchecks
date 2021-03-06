"""Basic sample for adding a healthcheck server to a Sanic application.
"""
from sanic import Sanic
from sanic.response import json

from sanic_healthchecks import start_healthcheck_server, healthcheck_response

APP = Sanic()


async def healthcheck_handler(_):
    """Demonstrates a simple healthcheck example.
    """
    data = {"status": "ok"}
    return healthcheck_response(data)


@APP.route("/")
async def root(_):
    """Boilerplate Sanic endpoint.
    """
    return json({"example_of": "a very simple healthcheck"})


if __name__ == "__main__":
    start_healthcheck_server(healthcheck_handler)
    APP.run(host="0.0.0.0", port=8000)
