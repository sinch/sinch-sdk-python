import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.internal import ListBatchesEndpoint
from sinch.domains.sms.models.v1.internal import ListBatchesRequest
from sinch.domains.sms.models.v1.response.list_batches_response import (
    ListBatchesResponse,
)
from datetime import datetime, timezone


@pytest.fixture
def request_data():
    return ListBatchesRequest(
        page=0,
        page_size=10,
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "count": 2,
            "page": 0,
            "page_size": 10,
            "batches": [
                {
                    "id": "01FC66621XXXXX119Z8PMV1QPQ",
                    "to": ["+46701234567"],
                    "from": "+46701111111",
                    "canceled": False,
                    "body": "Your verification code is 123456",
                    "type": "mt_text",
                    "created_at": "2024-06-06T09:22:14.304Z",
                    "modified_at": "2024-06-06T09:22:48.054Z",
                },
                {
                    "id": "01W4FFL35P4NC4K35SMSBATCH1",
                    "to": ["+46709876543"],
                    "from": "+46701111111",
                    "canceled": False,
                    "body": "Your order #12345 has been shipped",
                    "type": "mt_text",
                    "created_at": "2024-06-07T10:15:30.123Z",
                    "modified_at": "2024-06-07T10:15:35.456Z",
                },
            ],
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return ListBatchesEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/batches"
    )


def test_build_query_params_expects_all_params():
    """Test that query parameters are extracted correctly."""
    request_data = ListBatchesRequest(
        page=1,
        page_size=20,
        start_date=datetime(2024, 6, 1, tzinfo=timezone.utc),
        end_date=datetime(2024, 6, 30, tzinfo=timezone.utc),
        from_=["+46701111111", "+46702222222"],
        client_reference="test_ref_123",
    )

    endpoint = ListBatchesEndpoint("test_project_id", request_data)
    query_params = endpoint.build_query_params()

    assert query_params["page"] == 1
    assert query_params["page_size"] == 20
    assert query_params["from"] == ["+46701111111", "+46702222222"]
    assert query_params["client_reference"] == "test_ref_123"
    assert "start_date" in query_params
    assert "end_date" in query_params


def test_build_query_params_expects_excludes_none_values(request_data):
    """Test that None values are excluded from query parameters."""
    endpoint = ListBatchesEndpoint("test_project_id", request_data)
    query_params = endpoint.build_query_params()

    assert "start_date" not in query_params
    assert "end_date" not in query_params
    assert "from" not in query_params
    assert "client_reference" not in query_params
    assert query_params["page"] == 0
    assert query_params["page_size"] == 10


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is handled and mapped to the appropriate fields correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListBatchesResponse)
    assert parsed_response.count == 2
    assert parsed_response.page == 0
    assert parsed_response.page_size == 10
    assert parsed_response.batches is not None
    assert len(parsed_response.batches) == 2

    first_batch = parsed_response.batches[0]
    assert first_batch.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert first_batch.to == ["+46701234567"]
    assert first_batch.from_ == "+46701111111"
    assert first_batch.body == "Your verification code is 123456"
    assert first_batch.type == "mt_text"

    second_batch = parsed_response.batches[1]
    assert second_batch.id == "01W4FFL35P4NC4K35SMSBATCH1"
    assert second_batch.to == ["+46709876543"]
    assert second_batch.body == "Your order #12345 has been shipped"


def test_handle_response_expects_empty_batches_list():
    """Test that response with empty batches list is handled correctly."""
    request_data = ListBatchesRequest(page=0, page_size=10)
    endpoint = ListBatchesEndpoint("test_project_id", request_data)

    empty_response = HTTPResponse(
        status_code=200,
        body={
            "count": 0,
            "page": 0,
            "page_size": 10,
            "batches": [],
        },
        headers={"Content-Type": "application/json"},
    )

    parsed_response = endpoint.handle_response(empty_response)
    assert isinstance(parsed_response, ListBatchesResponse)
    assert parsed_response.count == 0
    assert parsed_response.batches == []
    assert len(parsed_response.content) == 0
