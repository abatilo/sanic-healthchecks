"""The core of running a healthcheck server on a different thread.

It's useful to run the healthchecks on a different web server entirely, because
it means that we're not going to take away any resources from the thread that
is running the actual Sanic application itself.

The healthchecks should report that the downstream and required dependencies of
a service are still accessible from the host or container that is running the
actual Sanic application.
"""
import asyncio
import json
import threading
from aiohttp import web


# Disabled because pylint incorrectly parses multiline arguments like this:
# https://github.com/PyCQA/pylint/issues/289
# pylint: disable=C0330
def healthcheck_response(
    data,
    *,
    text=None,
    body=None,
    status=200,
    reason=None,
    headers=None,
    content_type="application/json",
    dumps=json.dumps,
):
    """A response for a healthcheck."""
    return web.json_response(
        data,
        text=text,
        body=body,
        status=status,
        reason=reason,
        headers=headers,
        content_type=content_type,
        dumps=dumps,
    )


async def main(handler, host, port):
    """The main entrypoint for running an aiohttp server.

    This function will start an async compatible aiohttp server. There's no
    other fancy logic or configuration. The handler that is passed in will be
    available as an endpoint at the root path of whatever port gets specified.

    Requests will be made by sending an HTTP GET verb to:
    http://{host}:{port}/
    """
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    print(f"======= Listening for healthchecks on http://{host}:{port}/ ======")

    # pause here for very long time by serving HTTP requests and
    # waiting for keyboard interruption
    while True:
        await asyncio.sleep(100 * 3600)


def start_healthcheck_server(handler, host="0.0.0.0", port=8082):
    """Start the actual web server to respond to healthcheck requests.

    We need to make sure that this web server is non-blocking, so that the
    Sanic application can be instantiated as expected.
    """
    loop = asyncio.get_event_loop()
    httpd = threading.Thread(
        target=lambda: loop.run_until_complete(main(handler, host, port))
    )
    httpd.daemon = True
    httpd.start()
