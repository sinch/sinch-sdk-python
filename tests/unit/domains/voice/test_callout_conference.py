import json
import pytest
from sinch.domains.voice.enums import CalloutMethod

from sinch.domains.voice.endpoints.callouts.callout import CalloutEndpoint

from sinch.domains.voice.models.callouts.requests import ConferenceVoiceCalloutRequest


@pytest.fixture
def request_data():
    return ConferenceVoiceCalloutRequest(
        destination={
            "type": "number",
            "endpoint": "+33612345678",
        },
        cli="",
        greeting="Welcome",
        conferenceId="123456",
        conferenceDtmfOptions={"mode": "forward", "max_digits": 2, "timeout_mills": 2500},
        dtmf="dtmf",
        conference="conference",
        maxDuration=10,
        enableAce=True,
        enableDice=True,
        enablePie=True,
        locale="locale",
        mohClass="moh_class",
        custom="custom",
        domain="pstn",
    )


@pytest.fixture
def endpoint(request_data):
    return CalloutEndpoint(request_data, CalloutMethod.CONFERENCE.value)


@pytest.fixture
def mock_response_body():
    expected_body = {
        "method": "conferenceCallout",
        "conferenceCallout": {
            "destination": {"type": "number", "endpoint": "+33612345678"},
            "conferenceId": "123456",
            "cli": "",
            "conferenceDtmfOptions": {"mode": "forward", "timeoutMills": 2500, "maxDigits": 2},
            "dtmf": "dtmf",
            "conference": "conference",
            "maxDuration": 10,
            "enableAce": True,
            "enableDice": True,
            "enablePie": True,
            "locale": "locale",
            "greeting": "Welcome",
            "mohClass": "moh_class",
            "custom": "custom",
            "domain": "pstn",
        },
    }
    return json.dumps(expected_body)


def test_handle_response(endpoint, mock_response_body):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    request_body = endpoint.request_body()
    assert request_body == mock_response_body
