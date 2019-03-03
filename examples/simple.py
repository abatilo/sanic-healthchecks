"""Basic sample for adding a healthcheck server to a Sanic application.
"""
from sanic import Sanic
from sanic.response import json
from aiohttp import web

from sanic_healthchecks import start_healthcheck_server

APP = Sanic()


async def healthcheck_handler(_):
    """Demonstrates a simple healthcheck example.
    """
    data = {"status": "ok"}
    return web.json_response(data)


@APP.route("/")
async def root(_):
    """Boilerplate Sanic endpoint.
    """
    return json({"hello": "world"})


if __name__ == "__main__":
    start_healthcheck_server(healthcheck_handler)
    APP.run(host="0.0.0.0", port=8000)
