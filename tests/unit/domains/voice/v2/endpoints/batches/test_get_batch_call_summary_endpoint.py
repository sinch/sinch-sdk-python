import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.voice.api.v2.exceptions import VoiceException
from sinch.domains.voice.api.v2.internal.batches_endpoints import (
    GetBatchCallSummaryEndpoint,
)
from sinch.domains.voice.models.v2.batches.internal.request.batch_id_request import (
    BatchIdRequest,
)
from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)


@pytest.fixture
def request_data():
    return BatchIdRequest(batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC")


@pytest.fixture
def endpoint(request_data):
    return GetBatchCallSummaryEndpoint("test_project_id", request_data)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "batchId": "01BX5ZZKBKACTAV9WEVGEMMVRC",
            "sessionCount": 3,
            "queued": 1,
            "inProgress": 1,
            "completed": 1,
            "expired": 0,
            "requestedCps": 10,
            "ttlSeconds": 3600,
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "type": "https://api.sinch.com/docs/errors/not-found",
            "title": "Not Found",
            "detail": "The requested resource was not found.",
            "instance": "/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/batches/01BX5ZZKBKACTAV9WEVGEMMVRC",
        },
        headers={"Content-Type": "application/problem+json"},
    )


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_voice):
    """Test that the URL is built correctly, including the batch_id path param."""
    assert endpoint.build_url(mock_sinch_client_voice) == (
        "https://voice.api.sinch.com/v2/projects/test_project_id/batches/01BX5ZZKBKACTAV9WEVGEMMVRC"
    )


def test_request_body_expects_no_body(endpoint):
    """Test that a GET endpoint with only a path param produces no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is parsed and mapped into a BatchSummaryResponse correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, BatchSummaryResponse)
    assert parsed_response.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert parsed_response.session_count == 3
    assert parsed_response.queued == 1
    assert parsed_response.in_progress == 1
    assert parsed_response.completed == 1
    assert parsed_response.expired == 0
    assert parsed_response.requested_cps == 10
    assert parsed_response.ttl_seconds == 3600


def test_handle_response_expects_voice_exception_on_error(
    endpoint, mock_error_response
):
    """Test that VoiceException is raised when the server returns an error."""
    with pytest.raises(VoiceException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == (
        "Not Found: The requested resource was not found."
    )
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
