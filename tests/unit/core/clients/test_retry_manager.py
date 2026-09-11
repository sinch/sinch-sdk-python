import pytest
from unittest.mock import Mock
from sinch.core.clients.retry_configuration import RetryConfiguration
from sinch.core.clients.retry_manager import RetryManager
from sinch.core.enums import RetryPolicy
from sinch.core.models.http_response import HTTPResponse


def _response(status_code, headers=None):
    return HTTPResponse(status_code=status_code, headers=headers or {}, body={})


class TestExecute:
    def test_returns_immediately_on_a_non_retryable_status(self, mocker):
        no_sleep = mocker.patch("sinch.core.clients.retry_manager.time.sleep")
        manager = RetryManager(RetryConfiguration())
        call = Mock(return_value=_response(200))

        result = manager.execute(call)

        assert result.status_code == 200
        assert call.call_count == 1
        no_sleep.assert_not_called()

    def test_retries_a_429_until_it_succeeds(self, mocker):
        mocker.patch("sinch.core.clients.retry_manager.time.sleep")
        mocker.patch("sinch.core.clients.retry_manager.random.uniform", return_value=0.0)
        manager = RetryManager(RetryConfiguration())
        call = Mock(side_effect=[_response(429), _response(429), _response(200)])

        result = manager.execute(call)

        assert result.status_code == 200
        assert call.call_count == 3

    def test_gives_up_and_returns_the_last_response_after_max_retries(self, mocker):
        no_sleep = mocker.patch("sinch.core.clients.retry_manager.time.sleep")
        mocker.patch("sinch.core.clients.retry_manager.random.uniform", return_value=0.0)
        manager = RetryManager(RetryConfiguration(max_retries=3))
        call = Mock(return_value=_response(429))

        result = manager.execute(call)

        assert result.status_code == 429
        assert call.call_count == 4
        assert no_sleep.call_count == 3


class TestComputeDelay:
    def test_default_uses_retry_after_header_when_present(self, mocker):
        mocker.patch("sinch.core.clients.retry_manager.random.uniform", return_value=0.0)
        manager = RetryManager(RetryConfiguration())

        delay = manager._compute_delay(_response(429, {"Retry-After": "5"}), num_retries=0)

        assert delay == 5.0

    def test_default_falls_back_to_backoff_without_header(self, mocker):
        mocker.patch("sinch.core.clients.retry_manager.random.uniform", return_value=0.0)
        manager = RetryManager(RetryConfiguration(backoff_growth=4))

        assert manager._compute_delay(_response(429), num_retries=0) == 0.0

    def test_retry_after_only_ignores_backoff_when_header_missing(self):
        manager = RetryManager(RetryConfiguration(retry_policy=RetryPolicy.RETRY_AFTER))

        assert manager._compute_delay(_response(429), num_retries=0) is None

    def test_retry_after_only_honors_the_header_when_present(self, mocker):
        mocker.patch("sinch.core.clients.retry_manager.random.uniform", return_value=0.0)
        manager = RetryManager(RetryConfiguration(retry_policy=RetryPolicy.RETRY_AFTER))

        delay = manager._compute_delay(_response(429, {"Retry-After": "5"}), num_retries=0)

        assert delay == 5.0

    def test_backoff_ignores_retry_after_header(self, mocker):
        mocker.patch("sinch.core.clients.retry_manager.random.uniform", return_value=0.0)
        manager = RetryManager(RetryConfiguration(retry_policy=RetryPolicy.BACKOFF, backoff_growth=4))

        delay = manager._compute_delay(_response(429, {"Retry-After": "999"}), num_retries=0)

        assert delay == 0.0

    def test_backoff_exponential_growth(self):
        manager = RetryManager(RetryConfiguration(retry_policy=RetryPolicy.BACKOFF, backoff_growth=4))

        assert 0.0 <= manager._compute_delay(_response(429), num_retries=0) <= 1.0
        assert 0.0 <= manager._compute_delay(_response(429), num_retries=1) <= 4.0
        assert 0.0 <= manager._compute_delay(_response(429), num_retries=2) <= 16.0

    def test_none_never_retries(self):
        manager = RetryManager(RetryConfiguration(retry_policy=RetryPolicy.NONE))

        assert manager._compute_delay(_response(429, {"Retry-After": "5"}), num_retries=0) is None

    def test_retry_after_jitter_is_within_bounds(self):
        manager = RetryManager(RetryConfiguration())

        for _ in range(100):  # run many times to exercise the random range
            delay = manager._compute_delay(_response(429, {"Retry-After": "5"}), num_retries=0)
            assert 5.0 <= delay <= 5.0 + RetryManager.RETRY_AFTER_JITTER_SECONDS


class TestParseRetryAfter:
    @pytest.mark.parametrize("value,expected", [
        ("5", 5.0),
        ("0", 0.0),
        ("-3", None),
        ("abc", None),
        ("", None),
        (None, None),
        ("Wed, 21 Oct 2015 07:28:00 GMT", 0.0),
        ("Wed, 21 Oct 2015 07:28:00", 0.0),
    ])
    def test_parse_retry_after(self, value, expected):
        assert RetryManager._parse_retry_after(value) == expected
