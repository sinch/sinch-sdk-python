import pytest
from sinch.domains.numbers.endpoints.numbers_endpoint import NumbersEndpoint
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.domains.sms.endpoints.sms_endpoint import SMSEndpoint
from sinch.domains.authentication.endpoints.oauth import OAuthEndpoint

from sinch.domains.numbers.exceptions import NumbersException
from sinch.domains.conversation.exceptions import ConversationException
from sinch.domains.sms.exceptions import SMSException
from sinch.domains.authentication.exceptions import AuthenticationException


def test_numbers_endpoint_error_handling(project_id, http_response):
    numbers_endpoint = NumbersEndpoint(
        project_id=project_id,
        request_data={}
    )
    with pytest.raises(NumbersException) as error:
        numbers_endpoint.handle_response(http_response)
        assert str(error) == http_response.body["error"]["message"]
        assert error.is_from_server is True
        assert error.response_status_code == http_response.status_code


def test_conversation_endpoint_error_handling(project_id, http_response):
    numbers_endpoint = ConversationEndpoint(
        project_id=project_id,
        request_data={}
    )
    with pytest.raises(ConversationException) as error:
        numbers_endpoint.handle_response(http_response)
        assert str(error) == http_response.body["error"]["message"]
        assert error.is_from_server is True
        assert error.response_status_code == http_response.status_code


def test_sms_endpoint_error_handling(sinch_client_sync, sms_http_response):
    numbers_endpoint = SMSEndpoint(
        request_data={},
        sinch=sinch_client_sync
    )
    with pytest.raises(SMSException) as error:
        numbers_endpoint.handle_response(sms_http_response)
        assert str(error) == sms_http_response.body["error"]["message"]
        assert error.is_from_server is True
        assert error.response_status_code == sms_http_response.status_code


def test_authentication_endpoint_error_handling(http_response):
    numbers_endpoint = OAuthEndpoint()
    with pytest.raises(AuthenticationException) as error:
        numbers_endpoint.handle_response(http_response)
        assert str(error) == http_response.body["error"]["message"]
        assert error.is_from_server is True
        assert error.response_status_code == http_response.status_code
