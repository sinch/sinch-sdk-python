"""Unit tests for Voice API v2 Sinch Events"""
import base64
import hashlib
import hmac
import json

import pytest

from sinch.domains.voice import Voice
from sinch.domains.voice.api.v2.sinch_events import SinchEvents
from sinch.domains.voice.models.v2.sinch_events import (
    MenuInput,
    VoiceSinchEventRequest,
    VoiceSinchEventResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call
from tests.conftest import generate_service_authentication_header

SERVICE_SECRET = "vSMHuHj8tEoa0lfWfBKqEQ=="
SERVICE_ID = "serviceKey"


@pytest.fixture
def voice_sinch_event():
    return SinchEvents()


@pytest.fixture
def valid_request():
    method = "POST"
    path = "/webhooks/voice-v2/call/answered"
    body = json.dumps({"event": "call.answered"})
    headers = {
        "content-type": "application/json; charset=utf-8",
        "x-timestamp": "2026-06-10T21:27:04.1466768Z",
    }
    headers["authorization"] = generate_service_authentication_header(method, path, headers, body, SERVICE_SECRET, SERVICE_ID)
    return method, path, headers, body


@pytest.fixture
def call_payload():
    return {
        "callId": "01AN4Z07BY79KA1307SR9X4MV3",
        "projectId": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        "serviceId": "a74b1566-0f18-4f8e-9c23-8e6b5df8fd3e",
        "sessionId": "01AN4Z07BY79KA1307SR9X4MV2",
        "direction": "INBOUND",
        "originationType": "PHONE",
        "callType": "PHONE",
        "from": {"type": "PHONE", "phone": {"number": "+14155552671"}},
        "to": {"type": "PHONE", "phone": {"number": "+46735224800"}},
        "callResult": "INITIATED",
        "startTime": "2025-06-01T10:00:00Z",
        "callRate": {"currencyCode": "USD", "amount": "0.0060"},
        "callResourceUrl": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01AN4Z07BY79KA1307SR9X4MV3",
    }


def test_voice_exposes_sinch_events(mock_sinch_client_voice):
    """Test that the domain class exposes a Voice Sinch Events handler."""
    assert isinstance(Voice(mock_sinch_client_voice).v2.sinch_events, SinchEvents)


def test_parse_event_dict_expects_sinch_event_request(voice_sinch_event, call_payload):
    """Test that parse_event accepts a dict and returns a VoiceSinchEventRequest."""
    event = voice_sinch_event.parse_event(
        {"event": "call.incoming", "call": call_payload}
    )
    assert isinstance(event, VoiceSinchEventRequest)
    assert event.event == "call.incoming"
    assert event.menu is None
    assert event.call == Call(**call_payload)


def test_parse_event_json_string_expects_sinch_event_request(voice_sinch_event, call_payload):
    """Test that parse_event accepts a JSON string."""
    payload_str = json.dumps({"event": "call.answered", "call": call_payload})
    event = voice_sinch_event.parse_event(payload_str)
    assert event.event == "call.answered"
    assert event.menu is None
    assert event.call == Call(**call_payload)


def test_parse_event_bytes_expects_sinch_event_request(voice_sinch_event, call_payload):
    """Test that parse_event accepts raw bytes and decodes using headers."""
    payload_bytes = json.dumps(
        {"event": "call.hangup", "call": call_payload}
    ).encode("utf-8")
    event = voice_sinch_event.parse_event(
        payload_bytes, headers={"content-type": "application/json; charset=utf-8"}
    )
    assert event.event == "call.hangup"
    assert event.menu is None
    assert event.call == Call(**call_payload)


def test_parse_event_webhook_prefix_expects_custom_event_prefix(voice_sinch_event, call_payload):
    """Test that parse_event renames a `call.webhook.*` event to `call.customEvent.*`."""
    event = voice_sinch_event.parse_event(
        {"event": "call.webhook.on-answer", "call": call_payload}
    )
    assert event.event == "call.customEvent.on-answer"


def test_parse_event_invalid_json_expects_value_error(voice_sinch_event):
    """Test that invalid JSON raises a ValueError."""
    with pytest.raises(ValueError, match="Failed to decode JSON"):
        voice_sinch_event.parse_event("not json")


def test_build_response_expects_sinch_event_response(voice_sinch_event):
    """Test that build_response returns a validated VoiceSinchEventResponse."""
    response = voice_sinch_event.build_response(
        commands=[
            {
                "command": "messages",
                "messages": [
                    {
                        "type": "SAY",
                        "say": {"text": "Goodbye.", "voiceName": "Emma"},
                    }
                ],
            },
            {"command": "hangup"},
        ]
    )
    assert isinstance(response, VoiceSinchEventResponse)
    assert len(response.commands) == 2


def test_build_incoming_call_response_expects_call_name_and_events(voice_sinch_event):
    """Test that build_incoming_call_response sets call_name and events on the response."""
    response = voice_sinch_event.build_incoming_call_response(
        commands=[{"command": "hangup"}],
        call_name="incoming",
        events={"on_hangup": [{"command": "hangup"}]},
    )
    assert isinstance(response, VoiceSinchEventResponse)
    assert response.call_name == "incoming"
    assert len(response.events.on_hangup) == 1
    assert response.events.on_hangup[0].command == "hangup"


def test_validate_authentication_header_expects_true_for_valid_signature(valid_request):
    """Test that a correctly signed request validates against the given secret and key."""
    voice_sinch_event = SinchEvents()
    method, path, headers, body = valid_request
    assert voice_sinch_event.validate_authentication_header(method, path, headers, body, SERVICE_ID, SERVICE_SECRET)


def test_serialize_response_expects_correct_serialization(voice_sinch_event):
    """Test that serialize_response dumps by alias and drops unset fields."""
    response = voice_sinch_event.build_incoming_call_response(
        commands=[{"command": "hangup"}],
        call_name="incoming",
    )
    serialized = voice_sinch_event.serialize_response(response)
    assert serialized == {
        "commands": [{"command": "hangup"}],
        "callName": "incoming",
    }
