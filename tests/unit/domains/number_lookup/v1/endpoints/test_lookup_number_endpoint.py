import json
from unittest.mock import MagicMock
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.number_lookup.api.v1.internal import LookupNumberEndpoint
from sinch.domains.number_lookup.models.v1.internal import LookupNumberRequest
from sinch.domains.number_lookup.models.v1.response import LookupNumberResponse


@pytest.fixture
def request_data():
    return LookupNumberRequest(
        number="+12312312312", features=["LineType", "SimSwap"]
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "line": {
                "carrier": "T-Mobile USA",
                "type": "Mobile",
                "mobileCountryCode": "310",
                "mobileNetworkCode": "260",
                "ported": True,
                "portingDate": "2000-01-01T00:00:00+00:00",
            },
            "simSwap": {"swapped": True, "swapPeriod": "SP24H"},
            "countryCode": "US",
            "traceId": "84c1fd4063c38d9f3900d06e56542d48",
            "number": "+12312312312",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return LookupNumberEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_number_lookup
):
    """Check if endpoint URL is constructed correctly."""
    expected_url = (
        "https://lookup.api.sinch.com/v2/projects/test_project_id/lookups"
    )
    assert endpoint.build_url(mock_sinch_client_number_lookup) == expected_url


def test_build_url_with_custom_domain_expects_overridden_url():
    """Check if endpoint URL uses custom domain when configured."""
    request_data = LookupNumberRequest(
        number="+12312312312", features=["LineType", "SimSwap"]
    )
    endpoint = LookupNumberEndpoint("test_project_id", request_data)
    
    class MockConfiguration:
        number_lookup_origin = "https://custom.lookup.domain.com"
        project_id = "test_project_id"
        transport = MagicMock()
        transport.request = MagicMock()
    
    class MockSinchClient:
        configuration = MockConfiguration()
    
    mock_sinch = MockSinchClient()
    
    expected_url = (
        "https://custom.lookup.domain.com/v2/projects/test_project_id/lookups"
    )
    assert endpoint.build_url(mock_sinch) == expected_url


def test_request_body_expects_correct_json(endpoint):
    """Check if request body is correctly serialized to JSON."""
    body = endpoint.request_body()
    parsed_body = json.loads(body)
    assert parsed_body["number"] == "+12312312312"
    assert parsed_body["features"] == ["LineType", "SimSwap"]


def test_request_body_with_rnd_options_expects_correct_json():
    """Check if request body includes RND options when provided."""
    request_data = LookupNumberRequest(
        number="+12312312312",
        features=["RND"],
        rnd_feature_options={"contact_date": "2025-01-01"},
    )
    endpoint = LookupNumberEndpoint("test_project_id", request_data)
    body = endpoint.request_body()
    parsed_body = json.loads(body)
    assert parsed_body["number"] == "+12312312312"
    assert parsed_body["features"] == ["RND"]
    assert parsed_body["rndFeatureOptions"] == {"contact_date": "2025-01-01"}


def test_request_body_excludes_none_expects_correct_json():
    """Check if None values are excluded from request body."""
    request_data = LookupNumberRequest(number="+12312312312")
    endpoint = LookupNumberEndpoint("test_project_id", request_data)
    body = endpoint.request_body()
    parsed_body = json.loads(body)
    assert "number" in parsed_body
    assert "features" not in parsed_body
    assert "rndFeatureOptions" not in parsed_body


def test_handle_response_success_expects_valid_response(
    endpoint, mock_response
):
    """Check if successful response is handled correctly."""
    response = endpoint.handle_response(mock_response)
    assert isinstance(response, LookupNumberResponse)
    assert response.number == "+12312312312"
    assert response.country_code == "US"
    assert response.trace_id == "84c1fd4063c38d9f3900d06e56542d48"
    assert response.line is not None
    assert response.line.carrier == "T-Mobile USA"
    assert response.line.type == "Mobile"
    assert response.sim_swap is not None
    assert response.sim_swap.swapped is True
