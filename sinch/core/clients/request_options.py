from typing import Optional

from sinch.core.clients.internal.validation import (
    validate_timeout_seconds,
    validate_use_sinch_auth,
)
from sinch.core.clients.retry_configuration import RetryConfiguration


class RequestOptions:
    """
    Options applied to a single request, overriding the client level configuration.

    A value left to ``None`` falls back to the client configuration.

    :param timeout_seconds: Timeout in seconds for HTTP I/O operations. ``0`` disables it.
    :type timeout_seconds: Optional[float]
    :param use_sinch_auth: Whether the SDK authenticates the request. When ``False``, the SDK adds no
        ``Authorization`` header, whatever the authentication method, and requires no credentials.
    :type use_sinch_auth: Optional[bool]
    :param retry_configuration: Retry policy applied to rate-limited (HTTP 429) responses.
    :type retry_configuration: Optional[RetryConfiguration]
    :raises ValueError: If timeout_seconds is not a finite number or is negative, or use_sinch_auth is not a bool.
    """

    def __init__(
        self,
        timeout_seconds: Optional[float] = None,
        use_sinch_auth: Optional[bool] = None,
        retry_configuration: Optional[RetryConfiguration] = None,
    ):
        if timeout_seconds is not None:
            validate_timeout_seconds(timeout_seconds)
        if use_sinch_auth is not None:
            validate_use_sinch_auth(use_sinch_auth)

        self.timeout_seconds = timeout_seconds
        self.use_sinch_auth = use_sinch_auth
        self.retry_configuration = retry_configuration
