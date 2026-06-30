from datetime import datetime, timezone
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.core.pagination import SMSPaginator
from sinch.domains.sms.api.v1.inbounds_apis import Inbounds
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.api.v1.internal.inbounds_endpoints import (
    GetInboundEndpoint,
    ListInboundsEndpoint,
)
from sinch.domains.sms.models.v1.internal.inbound_id_request import InboundIdRequest
from sinch.domains.sms.models.v1.internal.list_inbounds_response import ListInboundsResponse
from sinch.domains.sms.models.v1.shared import MOTextMessage


@pytest.fixture
def mock_mo_text_response():
    """Sample MOTextMessage for testing."""
    return MOTextMessage(
        id="01FC66621XXXXX119Z8PMV1QPQ",
        from_="+46701234567",
        to="+46709876543",
        body="Test inbound message",
        type="mo_text",
        received_at=datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc),
    )


def test_inbounds_get_correct_request(
    mock_sinch_client_sms, mocker, mock_mo_text_response
):
    """Test that get sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = mock_mo_text_response

    spy_endpoint = mocker.spy(GetInboundEndpoint, "__init__")

    inbounds = Inbounds(mock_sinch_client_sms)
    response = inbounds.get(inbound_id="01FC66621XXXXX119Z8PMV1QPQ")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].inbound_id == "01FC66621XXXXX119Z8PMV1QPQ"

    assert isinstance(response, MOTextMessage)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_inbounds_list_correct_request(mock_sinch_client_sms, mocker):
    """Test that list sends the correct request and handles the response properly."""
    mock_response = ListInboundsResponse(count=1, page=0, page_size=2, inbounds=[])
    mock_sinch_client_sms.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(ListInboundsEndpoint, "__init__")

    inbounds = Inbounds(mock_sinch_client_sms)
    response = inbounds.list(
        page=0,
        page_size=2,
        to=["+46709876543"],
        start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2025, 1, 31, tzinfo=timezone.utc),
        client_reference="test_client_ref",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].page == 0
    assert kwargs["request_data"].page_size == 2
    assert kwargs["request_data"].to == ["+46709876543"]
    assert kwargs["request_data"].start_date == datetime(2025, 1, 1, tzinfo=timezone.utc)
    assert kwargs["request_data"].end_date == datetime(2025, 1, 31, tzinfo=timezone.utc)
    assert kwargs["request_data"].client_reference == "test_client_ref"

    assert isinstance(response, SMSPaginator)
    assert hasattr(response, "has_next_page")
    assert response.result == mock_response
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_sms_endpoint_handle_response_raises_exception_on_error(
    mock_sinch_client_sms,
):
    """
    Test that SmsEndpoint.handle_response raises SmsException when status_code >= 400.
    """
    request_data = InboundIdRequest(inbound_id="01FC66621XXXXX119Z8PMV1QPQ")
    endpoint = GetInboundEndpoint("test_project_id", request_data)

    error_response = HTTPResponse(status_code=400, body=1, headers={})

    with pytest.raises(SmsException) as exc_info:
        endpoint.handle_response(error_response)

    assert exc_info.value.args[0] == "Error 400"
    assert exc_info.value.http_response == error_response
    assert exc_info.value.is_from_server is True
    assert exc_info.value.response_status_code == 400


def test_inbounds_expects_validation_recalculates_auth_method_when_credentials_change(
    mock_sinch_client_sms, mock_mo_text_response
):
    """
    Test that SMS requests validate authentication and recalculate auth method
    when credentials change after initialization.
    """
    config = mock_sinch_client_sms.configuration

    assert config.authentication_method == "project_auth"

    config.transport.request.return_value = mock_mo_text_response
    config.sms_api_token = "test_sms_token"

    assert config.authentication_method == "project_auth"

    inbounds = Inbounds(mock_sinch_client_sms)
    response = inbounds.get(inbound_id="01FC66621XXXXX119Z8PMV1QPQ")

    assert config.authentication_method == "sms_auth"
    assert isinstance(response, MOTextMessage)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
