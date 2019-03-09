"""Basic sample for adding a healthcheck server to a Sanic application.
"""
import asyncio
from http import HTTPStatus
from sanic import Sanic
from sanic.response import json

from sanic_healthchecks import start_healthcheck_server, healthcheck_response

APP = Sanic()


async def healthcheck_task1():
    """A healthcheck representing a database check."""
    await asyncio.sleep(0.1)
    return ("database is good!", HTTPStatus.OK)


async def healthcheck_task2():
    """A healthcheck representing trying to send a request to another server."""
    await asyncio.sleep(0.15)
    return ("required service is good!", HTTPStatus.OK)


async def healthcheck_task3():
    """A healthcheck representing trying to verify valid AWS access."""
    await asyncio.sleep(0.5)
    return ("AWS credentials are good!", HTTPStatus.OK)


async def healthcheck_handler(_):
    """Demonstrates a simple healthcheck example.
    """
    tasks = (healthcheck_task1(), healthcheck_task2(), healthcheck_task3())
    responses = [
        {"message": msg, "status": status}
        for (msg, status) in await asyncio.gather(*tasks)
    ]
    overall_status = (
        200 if all(resp["status"].value == 200 for resp in responses) else 500
    )
    overall = {"status": overall_status, "responses": responses}
    return healthcheck_response(overall, status=overall_status)


@APP.route("/")
async def root(_):
    """Boilerplate Sanic endpoint.
    """
    return json({"example_of": "multiple healthchecks running concurrently"})


if __name__ == "__main__":
    start_healthcheck_server(healthcheck_handler)
    APP.run(host="0.0.0.0", port=8000)
