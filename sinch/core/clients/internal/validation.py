import math


def validate_timeout_seconds(timeout_seconds: float) -> None:
    """
    Validates a timeout, in seconds.

    :param timeout_seconds: The timeout to validate.
    :type timeout_seconds: float
    :raises ValueError: If timeout_seconds is not a finite number or is negative.
    """
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
    ):
        raise ValueError(f"timeout_seconds must be a finite number, got: {timeout_seconds}")
    if timeout_seconds < 0:
        raise ValueError(f"timeout_seconds must be zero or greater, got: {timeout_seconds}")


def validate_use_sinch_auth(use_sinch_auth: bool) -> None:
    """
    Validates the Sinch authentication flag.

    :param use_sinch_auth: The flag to validate.
    :type use_sinch_auth: bool
    :raises ValueError: If use_sinch_auth is not a bool.
    """
    if not isinstance(use_sinch_auth, bool):
        raise ValueError(f"use_sinch_auth must be a boolean, got: {use_sinch_auth}")
