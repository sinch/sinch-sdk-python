import pytest

from sinch import Client
from sinch.domains.authentication.models.authentication import OAuthToken
from sinch.domains.authentication.exceptions import AuthenticationException


def test_basic_auth_token_generation(sinch_client_sync):
    token = sinch_client_sync.authentication.get_auth_token()
    assert isinstance(token, OAuthToken)


def test_basic_auth_token_generation_invalid_credentials(project_id):
    sinch_client = Client(
        key_id="silly",
        key_secret="walk",
        project_id=project_id
    )
    with pytest.raises(AuthenticationException):
        sinch_client.authentication.get_auth_token()


def test_expired_token_refresh(sinch_client_sync, auth_token_as_dict):
    sinch_client_sync.authentication.set_auth_token(auth_token_as_dict)

    token = sinch_client_sync.authentication.get_auth_token()
    assert isinstance(token, OAuthToken)


async def test_basic_auth_token_generation_async(sinch_client_async):
    token = await sinch_client_async.authentication.get_auth_token()
    assert isinstance(token, OAuthToken)


def test_basic_auth_token_generation_sync(sinch_client_sync):
    token = sinch_client_sync.authentication.get_auth_token()
    assert isinstance(token, OAuthToken)
