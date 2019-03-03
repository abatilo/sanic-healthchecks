"""Top level package definition for sanic_healthchecks

Includes import for running a healthcheck server on a different thread
"""
from sanic_healthchecks.core import start_healthcheck_server

__all__ = ["start_healthcheck_server"]
