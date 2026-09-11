import random
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Callable, Optional

from sinch.core.clients.retry_configuration import RetryConfiguration
from sinch.core.enums import RetryPolicy
from sinch.core.models.http_response import HTTPResponse


class RetryManager:
    """Retries a call while the configured policy keeps returning a delay."""

    RETRYABLE_STATUS_CODES = frozenset({429})
    BACKOFF_BASE_SECONDS = 1.0
    RETRY_AFTER_JITTER_SECONDS = 0.25

    def __init__(self, configuration: RetryConfiguration):
        self.configuration = configuration

    def execute(self, call: Callable[[], HTTPResponse]) -> HTTPResponse:
        """
        Performs the call, retrying a rate-limited response for as long as the
        configured policy allows.

        :param call: The request to perform.
        :type call: Callable[[], HTTPResponse]
        :returns: The response from the last attempt.
        :rtype: HTTPResponse
        """
        num_retries = 0
        while True:
            http_response = call()
            if http_response.status_code not in self.RETRYABLE_STATUS_CODES:
                return http_response
            if num_retries >= self.configuration.max_retries:
                return http_response

            delay = self._compute_delay(http_response, num_retries)
            if delay is None:
                return http_response

            time.sleep(delay)
            num_retries += 1

    def _compute_delay(self, http_response: HTTPResponse, num_retries: int) -> Optional[float]:
        """
        Computes the delay before the next retry, or None if the configured
        policy declines to retry this response.

        :param http_response: The rate-limited response received.
        :type http_response: HTTPResponse
        :param num_retries: Number of retries already performed.
        :type num_retries: int
        :returns: The delay in seconds, or None to stop retrying.
        :rtype: Optional[float]
        """
        policy = self.configuration.retry_policy

        if policy == RetryPolicy.NONE:
            return None

        if policy != RetryPolicy.BACKOFF:
            headers = {key.lower(): value for key, value in http_response.headers.items()}
            retry_after_seconds = self._parse_retry_after(headers.get("retry-after"))
            if retry_after_seconds is not None:
                return retry_after_seconds + random.uniform(0, self.RETRY_AFTER_JITTER_SECONDS)
            if policy == RetryPolicy.RETRY_AFTER:
                return None

        max_delay = self.BACKOFF_BASE_SECONDS * (self.configuration.backoff_growth ** num_retries)
        return random.uniform(0, max_delay)

    @staticmethod
    def _parse_retry_after(value: Optional[str]) -> Optional[float]:
        """
        Parses the Retry-After header into a delay in seconds, or None if absent/unparseable.

        :param value: The raw header value.
        :type value: Optional[str]
        :returns: The delay in seconds, or None if absent/invalid.
        :rtype: Optional[float]
        """
        if not value:
            return None

        try:
            seconds = float(value)
            return seconds if seconds >= 0 else None
        except ValueError:
            pass

        try:
            retry_at = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=timezone.utc)
        return max(0.0, (retry_at - datetime.now(timezone.utc)).total_seconds())
