import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.authentication.endpoints.v1.oauth import OAuthEndpoint
from sinch.domains.authentication.exceptions import AuthenticationException


def test_handle_response_with_error_status_and_empty_body_raises_authentication_exception():
    response = HTTPResponse(status=401, headers={}, content=b"")

    with pytest.raises(AuthenticationException) as exc_info:
        OAuthEndpoint().handle_response(response)

    assert exc_info.value.response_status_code == 401
