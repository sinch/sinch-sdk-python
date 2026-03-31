import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import CancelBatchMessageEndpoint
from sinch.domains.sms.models.v1.internal import BatchIdRequest
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
            "to": ["12017777777"],
            "from": "12015555555",
            "canceled": True,
            "body": "SMS body message",
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
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "code": 404,
            "text": "Batch not found",
            "status": "NotFound",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return CancelBatchMessageEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/batches/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_build_url_with_different_batch_id(mock_sinch_client_sms):
    """Test that the URL is built correctly with different batch_id."""
    request_data = BatchIdRequest(batch_id="01W4FFL35P4NC4K35SMSBATCH1")
    endpoint = CancelBatchMessageEndpoint("test_project_id", request_data)

    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/batches/01W4FFL35P4NC4K35SMSBATCH1"
    )


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, TextResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.to == ["12017777777"]
    assert parsed_response.from_ == "12015555555"
    assert parsed_response.canceled is True
    assert parsed_response.body == "SMS body message"
    assert parsed_response.type == "mt_text"
    assert parsed_response.delivery_report == "full"
    assert parsed_response.feedback_enabled is True
    assert parsed_response.flash_message is False

    expected_created_at = datetime(
        2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
    )
    expected_modified_at = datetime(
        2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
    )
    expected_send_at = datetime(2024, 6, 6, 9, 25, 0, tzinfo=timezone.utc)
    expected_expire_at = datetime(2024, 6, 9, 9, 25, 0, tzinfo=timezone.utc)

    assert parsed_response.created_at == expected_created_at
    assert parsed_response.modified_at == expected_modified_at
    assert parsed_response.send_at == expected_send_at
    assert parsed_response.expire_at == expected_expire_at


def test_handle_response_expects_sms_exception_on_error(
    endpoint, mock_error_response
):
    """
    Test that SmsException is raised when server returns an error.
    """
    with pytest.raises(SmsException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404


def test_handle_response_expects_canceled_batch(endpoint):
    """
    Test that a canceled batch response is correctly parsed.
    """
    canceled_response = HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "to": ["12017777777"],
            "from": "12015555555",
            "canceled": True,
            "body": "SMS body message",
            "type": "mt_text",
            "created_at": "2024-06-06T09:22:14.304Z",
            "modified_at": "2024-06-06T09:22:48.054Z",
        },
        headers={"Content-Type": "application/json"},
    )

    parsed_response = endpoint.handle_response(canceled_response)
    assert parsed_response.canceled is True
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
