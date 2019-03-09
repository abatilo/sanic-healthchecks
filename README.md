# sanic-healthchecks
[![CircleCI](https://img.shields.io/circleci/project/github/abatilo/sanic-healthchecks.svg)](https://circleci.com/gh/abatilo/sanic-healthchecks)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPI version](https://badge.fury.io/py/sanic-healthchecks.svg)](https://badge.fury.io/py/sanic-healthchecks)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/sanic-healthchecks.svg)](https://pypi.python.org/pypi/sanic-healthchecks/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sanic-healthchecks.svg)

sanic-healthchecks makes it easy for you to start a healthcheck server on a
different thread than your actual Sanic application.

## Installation

`pip3 install sanic-healthchecks`

## Healthcheck Example
```python
from sanic import Sanic
from sanic.response import json

from sanic_healthchecks import start_healthcheck_server, healthcheck_response

APP = Sanic()


async def healthcheck_handler(_):
    data = {"status": "ok"}
    return healthcheck_response(data)


@APP.route("/")
async def root(_):
    return json({"example_of": "a very simple healthcheck"})


if __name__ == "__main__":
    start_healthcheck_server(healthcheck_handler)
    APP.run(host="0.0.0.0", port=8000)
```

Your Sanic application will now respond on to healthchecks on a different port:
```
⇒  curl http://localhost:8000 -i
HTTP/1.1 200 OK
Connection: keep-alive
Keep-Alive: 5
Content-Length: 17
Content-Type: application/json

{"hello":"world"}

⇒  curl http://localhost:8082 -i
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 16
Date: Sun, 03 Mar 2019 20:55:52 GMT
Server: Python/3.7 aiohttp/3.5.4

{"status": "ok"}
```

## Changelog
[Release Changelogs.](https://github.com/abatilo/sanic-healthchecks/blob/master/CHANGELOG.md)

## License
[Apache 2.0](https://github.com/abatilo/sanic-healthchecks/blob/master/LICENSE)

## But why?
Why would you want to run your healthchecks on a different thread, as opposed to creating another endpoint on your actual Sanic server?

Great question, internet stranger, and I have a few answers.

By running your healthchecks separately, we maintain a strong separation of
concerns. Since Sanic runs on a single thread, then any time you need to
respond to healthchecks, you're actually taking compute time away from the
event loop that is powering the actual requests that your application is there
to serve. Likewise, the state of your actual application is not going to affect
the healthchecks. There's a few camps of thought on this subject.

Some people say that if your web service isn't capable of responding to your
healthcheck probe, then the service shouldn't be considered healthy. I can
totally understand and respect this perspective, and if this is how you feel,
then there's no need to use sanic-healthchecks.

On the other hand, if you're like me, you've convinced yourself that the point
of healthchecks isn't purely to determine if the service can respond, but also
to determine if your service has everything that it needs from downstream
dependencies. If your requests are taking so long that the readiness or
liveness probes are timing out, that could mean that your service is unhealthy,
but it also could be a symptom of services that have long running requests.

Since we can run the healthchecks on a different web server entirely, we have
the ability to check that all of the downstream dependencies, like databases
and other services, are available. This helps narrow the problems with why a
service might be in a degraded state.

I would even make an argument that an increase in response latency could be a
metric that you use for automatically scaling your service. Treating it as a
way to kill instances makes it much fuzzier in terms of how to interpret the
increase in latency.

Another great reason to run your healthchecks on a different server is so that
you can assign a different port to this new server. This is valuable because
your healthchecks might actually have debug information in them that should not
be exposed to the same groups of people who are able to consume the main
service. By putting healthchecks on a different port, you can make sure to map
your load balancer to **not** include this healthcheck port.
