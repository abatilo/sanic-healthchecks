import asyncio
import threading
from aiohttp import web


async def main(handler, host, port):
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    print(f"======= Serving on http://{host}:{port}/ ======")

    # pause here for very long time by serving HTTP requests and
    # waiting for keyboard interruption
    while True:
        await asyncio.sleep(100 * 3600)


def start_healthcheck_server(handler, host="0.0.0.0", port=8082):
    loop = asyncio.get_event_loop()
    httpd = threading.Thread(
        target=lambda: loop.run_until_complete(main(handler, host, port))
    )
    httpd.daemon = True
    httpd.start()
