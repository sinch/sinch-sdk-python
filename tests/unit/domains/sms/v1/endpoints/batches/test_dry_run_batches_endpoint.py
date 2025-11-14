import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import DryRunEndpoint
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.models.v1.internal.dry_run_request import (
    DryRunTextRequest,
    DryRunBinaryRequest,
    DryRunMediaRequest,
)
from sinch.domains.sms.models.v1.response.dry_run_response import (
    DryRunResponse,
)
from sinch.domains.sms.models.v1.shared import (
    DryRunPerRecipientDetails,
    MediaBody,
)


@pytest.fixture
def text_request_data():
    return DryRunTextRequest(
        to=["+46701234567", "+46709876543"],
        from_="+46701111111",
        body="Your verification code is 123456",
    )


@pytest.fixture
def binary_request_data():
    return DryRunBinaryRequest(
        to=["+46701234567"],
        from_="+46701111111",
        body="SGVsbG8gV29ybGQh",
        udh="06050423F423F4",
    )


@pytest.fixture
def media_request_data():
    return DryRunMediaRequest(
        to=["+46701234567"],
        from_="+46701111111",
        body=MediaBody(
            url="https://capybara.com/image.jpg",
            message="Check out this image!",
            subject="Image",
        ),
    )


@pytest.fixture
def mock_dry_run_response():
    return DryRunResponse(
        number_of_recipients=2,
        number_of_messages=1,
        per_recipient=[
            DryRunPerRecipientDetails(
                recipient="+46701234567",
                body="Your order #12345 has been shipped",
                number_of_parts=1,
                encoding="text",
            ),
            DryRunPerRecipientDetails(
                recipient="+46709876543",
                body="Reminder: Your appointment is tomorrow at 2 PM",
                number_of_parts=1,
                encoding="text",
            ),
        ],
    )


@pytest.fixture
def mock_dry_run_response_without_per_recipient():
    return DryRunResponse(
        number_of_recipients=2,
        number_of_messages=1,
        per_recipient=None,
    )


@pytest.fixture
def mock_http_response_for_dry_run():
    return HTTPResponse(
        status_code=200,
        body={
            "number_of_recipients": 2,
            "number_of_messages": 1,
            "per_recipient": [
                {
                    "recipient": "+46701234567",
                    "body": "Your order #12345 has been shipped",
                    "number_of_parts": 1,
                    "encoding": "text",
                },
                {
                    "recipient": "+46709876543",
                    "body": "Reminder: Your appointment is tomorrow at 2 PM",
                    "number_of_parts": 1,
                    "encoding": "text",
                },
            ],
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_http_response_without_per_recipient():
    return HTTPResponse(
        status_code=200,
        body={
            "number_of_recipients": 2,
            "number_of_messages": 1,
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(text_request_data):
    return DryRunEndpoint("test_project_id", text_request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_sms):
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/batches/dry_run"
    )


def test_build_query_params_expects_per_recipient_and_number_of_recipients(
    text_request_data,
):
    """Test that query parameters are extracted correctly."""
    text_request_data.per_recipient = True
    text_request_data.number_of_recipients = 100

    endpoint = DryRunEndpoint("test_project_id", text_request_data)
    query_params = endpoint.build_query_params()

    assert query_params == {"per_recipient": True, "number_of_recipients": 100}


def test_build_query_params_expects_excludes_none_values(text_request_data):
    """Test that None values are excluded from query parameters."""
    text_request_data.per_recipient = None
    text_request_data.number_of_recipients = None

    endpoint = DryRunEndpoint("test_project_id", text_request_data)
    query_params = endpoint.build_query_params()

    assert query_params == {}


def test_request_body_expects_excludes_query_params(text_request_data):
    """Test that query params are excluded from request body."""
    text_request_data.per_recipient = True
    text_request_data.number_of_recipients = 100

    endpoint = DryRunEndpoint("test_project_id", text_request_data)
    body = json.loads(endpoint.request_body())

    assert "per_recipient" not in body
    assert "number_of_recipients" not in body
    assert "to" in body
    assert "from" in body
    assert "body" in body
    assert body["type"] == "mt_text"


def test_request_body_expects_binary_request_data(binary_request_data):
    """Test that binary request body contains correct fields."""
    binary_request_data.per_recipient = False
    binary_request_data.number_of_recipients = None

    endpoint = DryRunEndpoint("test_project_id", binary_request_data)
    body = json.loads(endpoint.request_body())

    assert "per_recipient" not in body
    assert "number_of_recipients" not in body
    assert "to" in body
    assert "from" in body
    assert "body" in body
    assert "udh" in body
    assert body["type"] == "mt_binary"
    assert body["udh"] == "06050423F423F4"
    assert body["body"] == "SGVsbG8gV29ybGQh"


def test_request_body_expects_media_request_data(media_request_data):
    """Test that media request body contains correct fields."""
    media_request_data.per_recipient = True
    media_request_data.number_of_recipients = 50

    endpoint = DryRunEndpoint("test_project_id", media_request_data)
    body = json.loads(endpoint.request_body())

    assert "per_recipient" not in body
    assert "number_of_recipients" not in body
    assert "to" in body
    assert "from" in body
    assert "body" in body
    assert body["type"] == "mt_media"
    assert "url" in body["body"]
    assert "message" in body["body"]
    assert "subject" in body["body"]
    assert body["body"]["url"] == "https://capybara.com/image.jpg"
    assert body["body"]["message"] == "Check out this image!"
    assert body["body"]["subject"] == "Image"


def test_handle_response_expects_correct_mapping(
    endpoint, mock_http_response_for_dry_run
):
    """Test that response is correctly mapped to DryRunResponse."""
    parsed_response = endpoint.handle_response(mock_http_response_for_dry_run)

    assert isinstance(parsed_response, DryRunResponse)
    assert parsed_response.number_of_recipients == 2
    assert parsed_response.number_of_messages == 1
    assert parsed_response.per_recipient is not None
    assert len(parsed_response.per_recipient) == 2
    assert parsed_response.per_recipient[0].recipient == "+46701234567"
    assert (
        parsed_response.per_recipient[0].body
        == "Your order #12345 has been shipped"
    )
    assert parsed_response.per_recipient[0].number_of_parts == 1


def test_handle_response_expects_response_without_per_recipient(
    endpoint, mock_http_response_without_per_recipient
):
    """Test that response without per_recipient is handled correctly."""
    parsed_response = endpoint.handle_response(
        mock_http_response_without_per_recipient
    )

    assert isinstance(parsed_response, DryRunResponse)
    assert parsed_response.number_of_recipients == 2
    assert parsed_response.number_of_messages == 1
    assert parsed_response.per_recipient is None
