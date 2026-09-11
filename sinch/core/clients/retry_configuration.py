from sinch.core.enums import RetryPolicy


class RetryConfiguration:
    """
    Retry policy applied to rate-limited (HTTP 429) responses.

    :param retry_policy: Strategy used to compute the delay before a retry.
    :type retry_policy: RetryPolicy
    :param max_retries: Maximum retries performed on top of the initial attempt.
    :type max_retries: int
    :param backoff_growth: Growth factor for the exponential backoff ceiling.
    :type backoff_growth: int
    :raises ValueError: If max_retries or backoff_growth is out of range.
    """

    def __init__(
        self,
        retry_policy: RetryPolicy = RetryPolicy.DEFAULT,
        max_retries: int = 3,
        backoff_growth: int = 4,
    ):
        if max_retries < 0:
            raise ValueError(f"RetryConfiguration: max_retries must be zero or greater, got: {max_retries}")
        if backoff_growth < 1:
            raise ValueError(f"RetryConfiguration: backoff_growth must be one or greater, got: {backoff_growth}")

        self.retry_policy = retry_policy
        self.max_retries = max_retries
        self.backoff_growth = backoff_growth
