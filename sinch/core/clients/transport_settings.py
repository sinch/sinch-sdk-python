import math


class TransportSettings:
    """
    Transport level settings applied to every request the SDK sends.

    :param timeout_seconds: Timeout in seconds for HTTP I/O operations. ``0`` disables it.
    :type timeout_seconds: float
    :param use_sinch_auth: When ``True``, endpoints supporting it authenticate against the Sinch auth server.
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
        if not isinstance(timeout_seconds, (int, float)) or not math.isfinite(timeout_seconds):
            raise ValueError(f"TransportSettings: timeout_seconds must be a finite number, got: {timeout_seconds}")
        if timeout_seconds < 0:
            raise ValueError(f"TransportSettings: timeout_seconds must be zero or greater, got: {timeout_seconds}")
        if not isinstance(use_sinch_auth, bool):
            raise ValueError(f"TransportSettings: use_sinch_auth must be a boolean, got: {use_sinch_auth}")

        self.timeout_seconds = timeout_seconds
        self.use_sinch_auth = use_sinch_auth
