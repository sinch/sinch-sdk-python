""" Sinch Python SDK
To access Sinch resources, use the Sync or Async version of the Sinch Client.
"""
__version__ = "1.1.3"

from sinch.core.clients.sinch_client_sync import SinchClient
from sinch.core.clients.sinch_client_async import SinchClientAsync

__all__ = (SinchClient, SinchClientAsync)
