import threading
import time
import pytest
from unittest.mock import Mock

from sinch.core.token_manager import TokenManager
from sinch.domains.authentication.models.v1.authentication import OAuthToken
from sinch.core.exceptions import ValidationException


def test_token_manager_set_valid_auth_token(sinch_client_sync, auth_token_as_dict):
    token_manager = TokenManager(sinch_client_sync)
    token_manager.set_auth_token(auth_token_as_dict)
    assert isinstance(token_manager.get_auth_token(), OAuthToken)


def test_token_manager_set_invalid_auth_token(sinch_client_sync):
    token_manager = TokenManager(sinch_client_sync)
    with pytest.raises(ValidationException):
        token_manager.set_auth_token(
            {
                "Access?": "You shall not pass!"
            }
        )


def test_get_auth_token_and_check_if_cached(sinch_client_sync, auth_token):
    sinch_client_sync = Mock()
    sinch_client_sync.configuration.transport.request.return_value = auth_token
    token_manager = TokenManager(sinch_client_sync)
    access_token = token_manager.get_auth_token()

    assert isinstance(access_token, OAuthToken)
    assert token_manager.token is auth_token


def test_get_auth_token_fetches_once_under_concurrency(auth_token):
    num_threads = 20
    barrier = threading.Barrier(num_threads)
    sinch = Mock()

    def slow_fetch(endpoint):
        time.sleep(0.05)
        return auth_token

    sinch.configuration.transport.request.side_effect = slow_fetch

    token_manager = TokenManager(sinch)

    results = []

    def worker():
        barrier.wait()
        results.append(token_manager.get_auth_token())

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sinch.configuration.transport.request.call_count == 1
    assert all(result is auth_token for result in results)


def test_refresh_auth_token_renews_once_under_concurrency(auth_token):
    num_threads = 20
    barrier = threading.Barrier(num_threads)
    sinch = Mock()

    def slow_fetch(endpoint):
        time.sleep(0.05)
        return auth_token

    sinch.configuration.transport.request.side_effect = slow_fetch
    token_manager = TokenManager(sinch)
    token_manager.token = OAuthToken(
        access_token="old", expires_in=1, scope="", token_type="bearer"
    )

    results = []

    def worker():
        barrier.wait()
        results.append(token_manager.refresh_auth_token("old"))

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sinch.configuration.transport.request.call_count == 1
    assert all(result is auth_token for result in results)


def test_invalidate_expired_token_emits_deprecation_warning(sinch_client_sync):
    token_manager = TokenManager(sinch_client_sync)

    with pytest.warns(DeprecationWarning, match="invalidate_expired_token"):
        token_manager.invalidate_expired_token()


def test_handle_invalid_token_emits_deprecation_warning(sinch_client_sync):
    token_manager = TokenManager(sinch_client_sync)
    response = Mock()
    response.headers = {}

    with pytest.warns(DeprecationWarning, match="handle_invalid_token"):
        token_manager.handle_invalid_token(response)
