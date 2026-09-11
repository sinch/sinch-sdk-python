import pytest
from sinch.core.clients.retry_configuration import RetryConfiguration
from sinch.core.enums import RetryPolicy


class TestRetryConfiguration:
    def test_defaults(self):
        configuration = RetryConfiguration()

        assert configuration.retry_policy == RetryPolicy.DEFAULT
        assert configuration.max_retries == 3
        assert configuration.backoff_growth == 4

    def test_accepts_a_custom_policy(self):
        configuration = RetryConfiguration(retry_policy=RetryPolicy.BACKOFF)

        assert configuration.retry_policy == RetryPolicy.BACKOFF

    def test_rejects_negative_max_retries(self):
        with pytest.raises(ValueError, match="max_retries must be zero or greater, got: -1"):
            RetryConfiguration(max_retries=-1)

    def test_allows_zero_max_retries(self):
        assert RetryConfiguration(max_retries=0).max_retries == 0

    def test_rejects_backoff_growth_below_one(self):
        with pytest.raises(ValueError, match="backoff_growth must be one or greater, got: 0"):
            RetryConfiguration(backoff_growth=0)
