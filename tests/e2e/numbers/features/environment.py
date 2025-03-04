import os
import logging
import asyncio
from sinch import SinchClient, SinchClientAsync

def get_logger():
    """Creates and returns a logger instance for this module only."""
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    if not log.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        log.addHandler(handler)
        log.propagate = False

    return log

logger = get_logger()

def before_all(context):
    """
    Initializes the appropriate Sinch client based on the environment variable SINCH_CLIENT_MODE.
    If it's set to 'async', a single event loop is created for all tests.
    Otherwise, we use the synchronous client.
    """
    client_mode = os.getenv('SINCH_CLIENT_MODE', 'sync')

    logger.info(f" Running E2E tests in **{client_mode.upper()}** mode")

    client_params = {
        'project_id': 'tinyfrog-jump-high-over-lilypadbasin',
        'key_id': 'keyId',
        'key_secret': 'keySecret',
    }
    if client_mode == 'async':
        # Create and set a single event loop for the entire test run
        context.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(context.loop)
        context.sinch = SinchClientAsync(**client_params)
    else:
        # Sync client does not need an event loop
        context.sinch = SinchClient(**client_params)
    context.sinch.configuration.auth_origin = 'http://localhost:3011'
    context.sinch.configuration.numbers_origin = 'http://localhost:3013'

def after_all(context):
    """
    Closes the Async event loop if it was created during the test
    """
    if hasattr(context, 'loop'):
        context.loop.close()