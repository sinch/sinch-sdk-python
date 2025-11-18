import json
import pytest
from datetime import datetime, timezone
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import UpdateBatchMessageEndpoint
from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
    UpdateTextRequestWithBatchId,
    UpdateBinaryRequestWithBatchId,
    UpdateMediaRequestWithBatchId,
)
from sinch.domains.sms.models.v1.shared.text_response import TextResponse
from sinch.domains.sms.models.v1.shared import MediaBody


@pytest.fixture
def text_request_data():
    return UpdateTextRequestWithBatchId(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        body="Updated verification code: 789012",
    )


@pytest.fixture
def binary_request_data():
    return UpdateBinaryRequestWithBatchId(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        udh="06050423F423F4",
        body="VXBkYXRlZCBiaW5hcnkgZGF0YQ==",
    )


@pytest.fixture
def media_request_data():
    return UpdateMediaRequestWithBatchId(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        body=MediaBody(
            url="https://capybara.com/updated-image.jpg",
            message="Updated image message!",
            subject="Updated Image",
        ),
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "to": ["+46701234567"],
            "from": "+46701111111",
            "canceled": False,
            "body": "Updated verification code: 789012",
            "type": "mt_text",
            "created_at": "2024-06-06T09:22:14.304Z",
            "modified_at": "2024-06-06T10:30:00.123Z",
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
    return UpdateBatchMessageEndpoint("test_project_id", text_request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/batches/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_request_body_expects_excludes_batch_id(text_request_data):
    """Test that batch_id is excluded from request body."""
    endpoint = UpdateBatchMessageEndpoint("test_project_id", text_request_data)
    body = json.loads(endpoint.request_body())

    assert "batch_id" not in body
    assert "body" in body
    assert body["body"] == "Updated verification code: 789012"


def test_request_body_expects_text_request_data(text_request_data):
    """Test that text request body contains correct fields."""
    text_request_data.from_ = "+46702222222"
    text_request_data.to_add = ["+46709999999"]
    text_request_data.to_remove = ["+46708888888"]

    endpoint = UpdateBatchMessageEndpoint("test_project_id", text_request_data)
    body = json.loads(endpoint.request_body())

    assert "batch_id" not in body
    assert body["from"] == "+46702222222"
    assert body["to_add"] == ["+46709999999"]
    assert body["to_remove"] == ["+46708888888"]
    assert body["body"] == "Updated verification code: 789012"


def test_request_body_expects_binary_request_data(binary_request_data):
    """Test that binary request body contains correct fields."""
    binary_request_data.from_ = "+46702222222"
    binary_request_data.to_add = ["+46709999999"]

    endpoint = UpdateBatchMessageEndpoint(
        "test_project_id", binary_request_data
    )
    body = json.loads(endpoint.request_body())

    assert "batch_id" not in body
    assert "udh" in body
    assert body["type"] == "mt_binary"
    assert body["udh"] == "06050423F423F4"
    assert body["body"] == "VXBkYXRlZCBiaW5hcnkgZGF0YQ=="
    assert body["from"] == "+46702222222"
    assert body["to_add"] == ["+46709999999"]


def test_request_body_expects_media_request_data(media_request_data):
    """Test that media request body contains correct fields."""
    media_request_data.from_ = "+46702222222"
    media_request_data.to_add = ["+46709999999"]

    endpoint = UpdateBatchMessageEndpoint(
        "test_project_id", media_request_data
    )
    body = json.loads(endpoint.request_body())

    assert "batch_id" not in body
    assert "body" in body
    assert body["type"] == "mt_media"
    assert "url" in body["body"]
    assert "message" in body["body"]
    assert "subject" in body["body"]
    assert body["body"]["url"] == "https://capybara.com/updated-image.jpg"
    assert body["body"]["message"] == "Updated image message!"
    assert body["body"]["subject"] == "Updated Image"
    assert body["from"] == "+46702222222"
    assert body["to_add"] == ["+46709999999"]


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is handled and mapped to the appropriate fields correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, TextResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.to == ["+46701234567"]
    assert parsed_response.from_ == "+46701111111"
    assert parsed_response.canceled is False
    assert parsed_response.body == "Updated verification code: 789012"
    assert parsed_response.type == "mt_text"
    assert parsed_response.delivery_report == "full"
    assert parsed_response.feedback_enabled is True
    assert parsed_response.flash_message is False

    assert parsed_response.created_at == datetime(
        2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
    )
    assert parsed_response.modified_at == datetime(
        2024, 6, 6, 10, 30, 0, 123000, tzinfo=timezone.utc
    )
    assert parsed_response.send_at == datetime(
        2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc
    )
    assert parsed_response.expire_at == datetime(
        2024, 6, 9, 9, 25, 0, tzinfo=timezone.utc
    )
