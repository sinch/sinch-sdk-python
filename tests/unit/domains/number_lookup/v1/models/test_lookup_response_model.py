from datetime import datetime, timezone
from sinch.domains.number_lookup.models.v1.response import (
    LookupNumberResponse,
)


def test_lookup_number_response_minimal_expects_valid_response():
    """Test minimal lookup response."""
    response_data = {
        "number": "+15551234567",
        "countryCode": "US",
        "traceId": "test-trace-id",
    }
    response = LookupNumberResponse.model_validate(response_data)
    assert response.number == "+15551234567"
    assert response.country_code == "US"
    assert response.trace_id == "test-trace-id"
    assert response.line is None
    assert response.sim_swap is None
    assert response.voip_detection is None
    assert response.rnd is None


def test_lookup_number_response_with_line_info_expects_valid_response():
    """Test lookup response with line information."""
    response_data = {
        "number": "+15552345678",
        "line": {
            "carrier": "T-Mobile USA",
            "type": "Mobile",
            "mobileCountryCode": "310",
            "mobileNetworkCode": "260",
            "ported": True,
            "portingDate": "2024-06-15T14:30:00+00:00",
        },
    }
    response = LookupNumberResponse.model_validate(response_data)
    assert response.line is not None
    assert response.line.carrier == "T-Mobile USA"
    assert response.line.type == "Mobile"
    assert response.line.mobile_country_code == "310"
    assert response.line.mobile_network_code == "260"
    assert response.line.ported is True
    assert response.line.porting_date == datetime(
        2024, 6, 15, 14, 30, 0, tzinfo=timezone.utc
    )


def test_lookup_number_response_with_sim_swap_expects_valid_response():
    """Test lookup response with SIM swap information."""
    response_data = {
        "number": "+15553456789",
        "simSwap": {"swapped": True, "swapPeriod": "SP24H"},
    }
    response = LookupNumberResponse.model_validate(response_data)
    assert response.sim_swap is not None
    assert response.sim_swap.swapped is True
    assert response.sim_swap.swap_period == "SP24H"


def test_lookup_number_response_with_voip_detection_expects_valid_response():
    """Test lookup response with VoIP detection information."""
    response_data = {
        "number": "+15554567890",
        "voIPDetection": {"probability": "High"},
    }
    response = LookupNumberResponse.model_validate(response_data)
    assert response.voip_detection.probability == "High"


def test_lookup_number_response_with_rnd_expects_valid_response():
    """Test lookup response with RND information."""
    response_data = {"number": "+15555678901", "rnd": {"disconnected": True}}
    response = LookupNumberResponse.model_validate(response_data)
    assert response.rnd is not None
    assert response.rnd.disconnected is True


def test_lookup_number_response_with_errors_expects_valid_response():
    """Test lookup response with error information."""
    response_data = {
        "number": "+15556789012",
        "line": {"error": {"code": "ERROR_CODE", "message": "Error message"}},
        "simSwap": {
            "error": {"code": "ERROR_CODE_2", "message": "Error message 2"}
        },
    }
    response = LookupNumberResponse.model_validate(response_data)
    assert response.line.error is not None
    assert response.line.error.code == "ERROR_CODE"
    assert response.line.error.message == "Error message"
    assert response.sim_swap.error is not None
    assert response.sim_swap.error.code == "ERROR_CODE_2"


def test_lookup_number_response_full_expects_valid_response():
    """Test complete lookup response with all features."""
    response_data = {
        "line": {
            "carrier": "T-Mobile USA",
            "type": "Mobile",
            "mobileCountryCode": "310",
            "mobileNetworkCode": "260",
            "ported": True,
            "portingDate": "2024-08-20T10:15:30+00:00",
        },
        "simSwap": {"swapped": True, "swapPeriod": "SP24H"},
        "voIPDetection": {"probability": "High"},
        "rnd": {"disconnected": True},
        "countryCode": "US",
        "traceId": "84c1fd4063c38d9f3900d06e56542d48",
        "number": "+15557890123",
    }
    response = LookupNumberResponse.model_validate(response_data)
    assert response.number == "+15557890123"
    assert response.country_code == "US"
    assert response.trace_id == "84c1fd4063c38d9f3900d06e56542d48"
    assert response.line is not None
    assert response.sim_swap is not None
    assert response.voip_detection is not None
    assert response.rnd is not None
