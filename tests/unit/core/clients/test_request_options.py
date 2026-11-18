import pytest

from sinch.core.clients.request_options import RequestOptions
from sinch.core.clients.retry_configuration import RetryConfiguration


def test_request_options_expects_every_field_unset_by_default():
    options = RequestOptions()

    assert options.timeout_seconds is None
    assert options.use_sinch_auth is None
    assert options.retry_configuration is None


def test_request_options_expects_given_values():
    retry_configuration = RetryConfiguration(max_retries=1)

    options = RequestOptions(
        timeout_seconds=0,
        use_sinch_auth=False,
        retry_configuration=retry_configuration,
    )

    assert options.timeout_seconds == 0
    assert options.use_sinch_auth is False
    assert options.retry_configuration is retry_configuration


@pytest.mark.parametrize(
    "timeout_seconds", [-1, float("inf"), float("nan"), "10", True]
)
def test_request_options_with_invalid_timeout_expects_value_error(
    timeout_seconds,
):
    with pytest.raises(ValueError, match="timeout_seconds"):
        RequestOptions(timeout_seconds=timeout_seconds)


@pytest.mark.parametrize("use_sinch_auth", [0, 1, "false"])
def test_request_options_with_non_bool_use_sinch_auth_expects_value_error(
    use_sinch_auth,
):
    with pytest.raises(ValueError, match="use_sinch_auth"):
        RequestOptions(use_sinch_auth=use_sinch_auth)
