from sinch.core.clients.internal.validation import (
    validate_timeout_seconds,
    validate_use_sinch_auth,
)


class TransportSettings:
    """
    Transport level settings applied to every request the SDK sends.

    :param timeout_seconds: Timeout in seconds for HTTP I/O operations. ``0`` disables it.
    :type timeout_seconds: float
    :param use_sinch_auth: Whether the SDK authenticates the requests. When ``False``, the SDK adds no
        ``Authorization`` header, whatever the authentication method, and requires no credentials.
    :type use_sinch_auth: bool
    :raises ValueError: If timeout_seconds is not a finite number or is negative, or use_sinch_auth is not a bool.
    """

    DEFAULT_TIMEOUT_SECONDS = 60
    DEFAULT_USE_SINCH_AUTH = True

    def __init__(
        self,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        use_sinch_auth: bool = DEFAULT_USE_SINCH_AUTH,
    ):
        validate_timeout_seconds(timeout_seconds)
        validate_use_sinch_auth(use_sinch_auth)

        self.timeout_seconds = timeout_seconds
        self.use_sinch_auth = use_sinch_auth
