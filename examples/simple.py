from sanic import Sanic
from sanic.response import json
from aiohttp import web

from sanic_healthchecks import start_healthcheck_server

app = Sanic()


async def handler(request):
    """Demonstrates a simple healthcheck example.
    """
    data = {"status": "ok"}
    return web.json_response(data)


@app.route("/")
async def root(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    start_healthcheck_server(handler)
    app.run(host="0.0.0.0", port=8000)
