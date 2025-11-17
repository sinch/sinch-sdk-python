import json
import pytest
from datetime import datetime, timezone
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import SendSMSEndpoint
from sinch.domains.sms.models.v1.shared.text_request import TextRequest
from sinch.domains.sms.models.v1.shared.binary_request import BinaryRequest
from sinch.domains.sms.models.v1.shared.media_request import MediaRequest
from sinch.domains.sms.models.v1.shared.text_response import TextResponse
from sinch.domains.sms.models.v1.shared import MediaBody


@pytest.fixture
def text_request_data():
    return TextRequest(
        to=["+46701234567", "+46709876543"],
        from_="+46701111111",
        body="Your verification code is 123456",
    )


@pytest.fixture
def binary_request_data():
    return BinaryRequest(
        to=["+46701234567"],
        from_="+46701111111",
        body="SGVsbG8gV29ybGQh",
        udh="06050423F423F4",
    )


@pytest.fixture
def media_request_data():
    return MediaRequest(
        to=["+46701234567"],
        from_="+46701111111",
        body=MediaBody(
            url="https://capybara.com/image.jpg",
            message="Check out this image!",
            subject="Image",
        ),
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=201,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "to": ["+46701234567", "+46709876543"],
            "from": "+46701111111",
            "canceled": False,
            "body": "Your verification code is 123456",
            "type": "mt_text",
            "created_at": "2024-06-06T09:22:14.304Z",
            "modified_at": "2024-06-06T09:22:14.304Z",
            "delivery_report": "full",
            "send_at": "2024-06-06T09:25:00Z",
            "expire_at": "2024-06-09T09:25:00Z",
            "feedback_enabled": True,
            "flash_message": False,
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(text_request_data):
    return SendSMSEndpoint("test_project_id", text_request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/batches"
    )


def test_request_body_expects_text_request_data(text_request_data):
    """Test that text request body contains correct fields."""
    endpoint = SendSMSEndpoint("test_project_id", text_request_data)
    body = json.loads(endpoint.request_body())

    assert "to" in body
    assert "from" in body
    assert "body" in body
    assert body["type"] == "mt_text"
    assert body["to"] == ["+46701234567", "+46709876543"]
    assert body["from"] == "+46701111111"
    assert body["body"] == "Your verification code is 123456"


def test_request_body_expects_binary_request_data(binary_request_data):
    """Test that binary request body contains correct fields."""
    endpoint = SendSMSEndpoint("test_project_id", binary_request_data)
    body = json.loads(endpoint.request_body())

    assert "to" in body
    assert "from" in body
    assert "body" in body
    assert "udh" in body
    assert body["type"] == "mt_binary"
    assert body["udh"] == "06050423F423F4"
    assert body["body"] == "SGVsbG8gV29ybGQh"


def test_request_body_expects_media_request_data(media_request_data):
    """Test that media request body contains correct fields."""
    endpoint = SendSMSEndpoint("test_project_id", media_request_data)
    body = json.loads(endpoint.request_body())

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


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is handled and mapped to the appropriate fields correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, TextResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.to == ["+46701234567", "+46709876543"]
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
        2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
    )
    assert parsed_response.send_at == datetime(
        2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc
    )
    assert parsed_response.expire_at == datetime(
        2024, 6, 9, 9, 25, 0, tzinfo=timezone.utc
    )
