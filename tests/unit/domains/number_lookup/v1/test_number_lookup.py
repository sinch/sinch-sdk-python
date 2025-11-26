from datetime import datetime, timezone
from sinch.domains.number_lookup.api.v1.number_lookup_apis import NumberLookup
from sinch.domains.number_lookup.api.v1.internal import LookupNumberEndpoint
from sinch.domains.number_lookup.models.v1.internal import LookupNumberRequest
from sinch.domains.number_lookup.models.v1.response import LookupNumberResponse
from sinch.domains.number_lookup.models.v1.shared import Line, SimSwap, VoIPDetection, Rnd
from sinch.domains.number_lookup.models.v1.types import RndFeatureOptionsDict


def test_lookup_expects_valid_request(mock_sinch_client_number_lookup, mocker):
    """
    Test that the NumberLookup.lookup() method sends the correct request
    and handles the response properly.
    """
    mock_response = LookupNumberResponse(
        number="+15551234567", country_code="US"
    )
    mock_sinch_client_number_lookup.configuration.transport.request.return_value = mock_response

    # Spy on the LookupNumberEndpoint to capture calls
    spy_endpoint = mocker.spy(LookupNumberEndpoint, "__init__")

    number_lookup = NumberLookup(mock_sinch_client_number_lookup)
    response = number_lookup.lookup("+15551234567")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == LookupNumberRequest(number="+15551234567")

    assert isinstance(response, LookupNumberResponse)
    assert response.number == "+15551234567"
    assert response.country_code == "US"
    mock_sinch_client_number_lookup.configuration.transport.request.assert_called_once()


def test_lookup_with_features_expects_valid_request(
    mock_sinch_client_number_lookup, mocker
):
    """
    Test that the NumberLookup.lookup() method with features sends the correct request
    and handles the response properly.
    """
    mock_response = LookupNumberResponse(
        number="+15552345678", country_code="US"
    )
    mock_sinch_client_number_lookup.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(LookupNumberEndpoint, "__init__")

    number_lookup = NumberLookup(mock_sinch_client_number_lookup)
    response = number_lookup.lookup(
        "+15552345678", features=["LineType", "SimSwap", "VoIPDetection"]
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == LookupNumberRequest(
        number="+15552345678",
        features=["LineType", "SimSwap", "VoIPDetection"],
    )

    assert isinstance(response, LookupNumberResponse)
    assert response.number == "+15552345678"
    mock_sinch_client_number_lookup.configuration.transport.request.assert_called_once()


def test_lookup_with_rnd_options_expects_valid_request(
    mock_sinch_client_number_lookup, mocker
):
    """
    Test that the NumberLookup.lookup() method with RND options sends the correct request
    and handles the response properly.
    """
    mock_response = LookupNumberResponse(
        number="+15553456789", country_code="US"
    )
    mock_sinch_client_number_lookup.configuration.transport.request.return_value = mock_response

    rnd_options: RndFeatureOptionsDict = {"contact_date": "2025-01-01"}
    spy_endpoint = mocker.spy(LookupNumberEndpoint, "__init__")

    number_lookup = NumberLookup(mock_sinch_client_number_lookup)
    response = number_lookup.lookup(
        "+15553456789", features=["RND"], rnd_feature_options=rnd_options
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == LookupNumberRequest(
        number="+15553456789",
        features=["RND"],
        rnd_feature_options=rnd_options,
    )

    assert isinstance(response, LookupNumberResponse)
    assert response.number == "+15553456789"
    mock_sinch_client_number_lookup.configuration.transport.request.assert_called_once()


def test_lookup_missing_project_id_expects_error():
    """
    Test that missing project_id raises an error.
    """
    from unittest.mock import Mock
    import pytest

    sinch = Mock()
    sinch.configuration = Mock()
    sinch.configuration.project_id = None

    number_lookup = NumberLookup(sinch)

    with pytest.raises(ValueError, match="project_id is required"):
        number_lookup.lookup("+15554567890")


def test_lookup_full_response_expects_valid_request(
    mock_sinch_client_number_lookup, mocker
):
    """
    Test that the NumberLookup.lookup() method with all features sends the correct request
    and handles the full response properly.
    """
    mock_response = LookupNumberResponse(
        number="+15555678901",
        country_code="US",
        trace_id="test-trace-id",
        line=Line(
            carrier="T-Mobile USA",
            type="Mobile",
            mobile_country_code="310",
            mobile_network_code="260",
            ported=True,
            porting_date=datetime(2024, 8, 20, 10, 15, 30, tzinfo=timezone.utc),
        ),
        sim_swap=SimSwap(swapped=True, swap_period="SP24H"),
        voip_detection=VoIPDetection(probability="High"),
        rnd=Rnd(disconnected=True),
    )
    mock_sinch_client_number_lookup.configuration.transport.request.return_value = mock_response

    spy_endpoint = mocker.spy(LookupNumberEndpoint, "__init__")

    number_lookup = NumberLookup(mock_sinch_client_number_lookup)
    response = number_lookup.lookup(
        "+15555678901",
        features=["LineType", "SimSwap", "VoIPDetection", "RND"],
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"] == LookupNumberRequest(
        number="+15555678901",
        features=["LineType", "SimSwap", "VoIPDetection", "RND"],
    )

    assert isinstance(response, LookupNumberResponse)
    assert response.number == "+15555678901"
    assert response.country_code == "US"
    assert response.trace_id == "test-trace-id"
    assert response.line is not None
    assert response.line.carrier == "T-Mobile USA"
    assert response.line.type == "Mobile"
    assert response.line.mobile_country_code == "310"
    assert response.line.mobile_network_code == "260"
    assert response.line.ported is True
    assert response.line.porting_date == datetime(2024, 8, 20, 10, 15, 30, tzinfo=timezone.utc)
    assert response.sim_swap.swapped is True
    assert response.sim_swap.swap_period == "SP24H"
    assert response.voip_detection is not None
    assert response.voip_detection.probability == "High"
    assert response.rnd is not None
    assert response.rnd.disconnected is True
    mock_sinch_client_number_lookup.configuration.transport.request.assert_called_once()
