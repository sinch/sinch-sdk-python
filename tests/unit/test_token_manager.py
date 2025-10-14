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
        token_manager.set_auth_token({"Access?": "You shall not pass!"})


def test_get_auth_token_and_check_if_cached(sinch_client_sync, auth_token):
    sinch_client_sync = Mock()
    sinch_client_sync.configuration.transport.request.return_value = auth_token
    token_manager = TokenManager(sinch_client_sync)
    access_token = token_manager.get_auth_token()

    assert isinstance(access_token, OAuthToken)
    assert token_manager.token is auth_token
