import pytest
from unittest.mock import Mock, AsyncMock

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.authentication.endpoints.oauth import OAuthEndpoint
from sinch.domains.authentication.exceptions import AuthenticationException


def test_handling_401_without_expiration(sinch_client_sync, auth_token_as_dict):
    http_response = HTTPResponse(
        status_code=401,
        headers={
            "wwww-authenticaiton": "Bearer error='invalid_token', error_description='Unable to parse token'"
        },
        body={}
    )
    sinch_client_sync.configuration.token_manager.set_auth_token(auth_token_as_dict)

    with pytest.raises(AuthenticationException):
        sinch_client_sync.configuration.transport.handle_response(
            http_response=http_response,
            endpoint=OAuthEndpoint()
        )


def test_handling_401_with_expired_token_gets_invalidated_and_refreshed(
    sinch_client_sync,
    auth_token_as_dict,
    expired_token_http_response
):
    sinch_client_sync.configuration.token_manager.set_auth_token(auth_token_as_dict)
    sinch_client_sync.configuration.transport.request = Mock()
    sinch_client_sync.configuration.transport.request.return_value = "Token Refresh!"

    transport_response = sinch_client_sync.configuration.transport.handle_response(
        http_response=expired_token_http_response,
        endpoint=OAuthEndpoint()
    )
    assert transport_response == "Token Refresh!"


async def test_handling_401_with_expired_token_gets_refreshed_async(
    sinch_client_async,
    auth_token_as_dict,
    expired_token_http_response
):
    sinch_client_async.configuration.token_manager.set_auth_token(auth_token_as_dict)
    sinch_client_async.configuration.transport.request = AsyncMock()
    sinch_client_async.configuration.transport.request.return_value = "Token Refresh!"

    transport_response = await sinch_client_async.configuration.transport.handle_response(
        http_response=expired_token_http_response,
        endpoint=OAuthEndpoint()
    )
    assert transport_response == "Token Refresh!"
