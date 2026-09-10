import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.shared.call import Call
from sinch.domains.voice.models.v2.sinch_events.menu_input import MenuInput
from sinch.domains.voice.models.v2.sinch_events.voice_sinch_event_request import (
    VoiceSinchEventRequest,
)

CALL = {
    "call_id": "01ARZ3NDEKTSV4RRFFQ69G5FAA",
    "project_id": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
    "service_id": "6e124178-c29d-46a5-943c-5c2ae544aade",
    "session_id": "01BX5ZZKBKACTAV9WEVGEMMVRB",
    "start_time": "2025-02-10T09:00:00Z",
    "call_type": "PHONE",
    "direction": "INBOUND",
    "call_result": "INITIATED",
    "origination_type": "PHONE",
    "call_rate": {"currency_code": "USD", "amount": "0.0123"},
    "call_resource_url": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
}


def test_voice_sinch_event_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = VoiceSinchEventRequest(
        event="call.menu",
        call=CALL,
        menu={"menu_name": "main", "input": "1"},
    )

    assert model.event == "call.menu"
    assert isinstance(model.call, Call)
    assert model.call.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert isinstance(model.menu, MenuInput)
    assert model.menu.menu_name == "main"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["event"] == "call.menu"
    assert alias_dump["call"]["callId"] == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert alias_dump["menu"]["menuName"] == "main"


def test_voice_sinch_event_request_expects_dynamic_custom_event_passthrough():
    """Test that a dynamic call.customEvent.* event name is accepted as-is."""
    model = VoiceSinchEventRequest(event="call.customEvent.menu-selection", call=CALL)

    assert model.event == "call.customEvent.menu-selection"


def test_voice_sinch_event_request_expects_optional_menu_defaults_to_none():
    """Test that the optional menu field defaults to None."""
    model = VoiceSinchEventRequest(event="call.incoming", call=CALL)

    assert model.menu is None


def test_voice_sinch_event_request_expects_webhook_prefix_renamed_to_custom_event():
    """Test that a wire `call.webhook.*` event name is renamed to `call.customEvent.*`."""
    model = VoiceSinchEventRequest(event="call.webhook.on-answer", call=CALL)

    assert model.event == "call.customEvent.on-answer"


def test_voice_sinch_event_request_expects_validation_error_for_missing_required():
    """Test that event and call are required."""
    with pytest.raises(ValidationError):
        VoiceSinchEventRequest()
