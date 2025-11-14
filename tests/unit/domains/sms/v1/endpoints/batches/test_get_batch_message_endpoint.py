import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import GetBatchMessageEndpoint
from sinch.domains.sms.models.v1.internal import BatchIdRequest
from sinch.domains.sms.models.v1.types import BatchResponse
from sinch.domains.sms.models.v1.shared.text_response import TextResponse
from sinch.domains.sms.api.v1.exceptions import SmsException
from datetime import datetime, timezone


@pytest.fixture
def request_data():
    return BatchIdRequest(batch_id="01FC66621XXXXX119Z8PMV1QPQ")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "to": ["+46701234567"],
            "from": "+46701111111",
            "canceled": False,
            "body": "Your verification code is 123456",
            "type": "mt_text",
            "created_at": "2024-06-06T09:22:14.304Z",
            "modified_at": "2024-06-06T09:22:48.054Z",
            "delivery_report": "full",
            "send_at": "2024-06-06T09:25:00Z",
            "expire_at": "2024-06-09T09:25:00Z",
            "feedback_enabled": True,
            "flash_message": False,
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return GetBatchMessageEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/batches/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is handled and mapped to the appropriate fields correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, TextResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.to == ["+46701234567"]
    assert parsed_response.from_ == "+46701111111"
    assert parsed_response.canceled is False
    assert parsed_response.body == "Your verification code is 123456"
    assert parsed_response.type == "mt_text"
    assert parsed_response.delivery_report == "full"
    assert parsed_response.feedback_enabled is True
    assert parsed_response.flash_message is False

    assert parsed_response.created_at == datetime(
        2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
    )
    assert parsed_response.modified_at == datetime(
        2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
    )
    assert parsed_response.send_at == datetime(
        2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc
    )
    assert parsed_response.expire_at == datetime(
        2024, 6, 9, 9, 25, 0, tzinfo=timezone.utc
    )
