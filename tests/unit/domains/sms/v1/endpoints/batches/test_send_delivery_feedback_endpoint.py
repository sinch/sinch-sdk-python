import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import DeliveryFeedbackEndpoint
from sinch.domains.sms.api.v1.exceptions import SmsException
from sinch.domains.sms.models.v1.internal import DeliveryFeedbackRequest


@pytest.fixture
def request_data():
    return DeliveryFeedbackRequest(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        recipients=["+46701234567", "+46709876543"],
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=204,
        body=None,
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return DeliveryFeedbackEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/batches/01FC66621XXXXX119Z8PMV1QPQ/delivery_feedback"
    )


def test_request_body_expects_correct_data(request_data):
    """Test that the request body contains correct fields."""
    endpoint = DeliveryFeedbackEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert "batch_id" in body
    assert "recipients" in body
    assert body["batch_id"] == "01FC66621XXXXX119Z8PMV1QPQ"
    assert body["recipients"] == ["+46701234567", "+46709876543"]


def test_request_body_expects_single_recipient():
    """Test that the request body works with a single recipient."""
    request_data = DeliveryFeedbackRequest(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        recipients=["+46701234567"],
    )
    endpoint = DeliveryFeedbackEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert body["recipients"] == ["+46701234567"]


def test_request_body_expects_empty_recipients():
    """Test that the request body works with empty recipients list."""
    request_data = DeliveryFeedbackRequest(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        recipients=[],
    )
    endpoint = DeliveryFeedbackEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert body["recipients"] == []


def test_handle_response_expects_success_with_empty_body():
    """Test that response with 200 status code and empty body is handled correctly."""
    request_data = DeliveryFeedbackRequest(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ",
        recipients=["+46701234567"],
    )
    endpoint = DeliveryFeedbackEndpoint("test_project_id", request_data)

    empty_response = HTTPResponse(
        status_code=200,
        body={},
        headers={"Content-Type": "application/json"},
    )

    result = endpoint.handle_response(empty_response)
    assert result is None
