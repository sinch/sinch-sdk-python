import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.events.internal.send_event_request import (
    SendEventRequest,
)
from sinch.domains.conversation.models.v1.events.shared.app_event import (
    ComposingAppEvent,
)


def test_send_event_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SendEventRequest(
        app_id="01EB37HMH1M6SV18ZNJMN108K1",
        recipient={"contact_id": "01EKA5J45DA8Y30K4DDX0A7Z6C"},
        event={"composing_event": {}},
        callback_url="https://my-server.com/events",
        channel_priority_order=["WHATSAPP"],
        event_metadata="metadata",
        queue="HIGH_PRIORITY",
    )

    assert model.app_id == "01EB37HMH1M6SV18ZNJMN108K1"
    assert model.recipient.contact_id == "01EKA5J45DA8Y30K4DDX0A7Z6C"
    assert isinstance(model.event, ComposingAppEvent)
    assert model.event.composing_event == {}
    assert model.event_destination_target == "https://my-server.com/events"
    assert model.channel_priority_order == ["WHATSAPP"]
    assert model.event_metadata == "metadata"
    assert model.queue == "HIGH_PRIORITY"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump["app_id"] == "01EB37HMH1M6SV18ZNJMN108K1"
    assert alias_dump["recipient"] == {
        "contact_id": "01EKA5J45DA8Y30K4DDX0A7Z6C"
    }
    assert alias_dump["event"] == {"composing_event": {}}
    assert alias_dump["callback_url"] == "https://my-server.com/events"
    assert alias_dump["channel_priority_order"] == ["WHATSAPP"]
    assert alias_dump["event_metadata"] == "metadata"
    assert alias_dump["queue"] == "HIGH_PRIORITY"


def test_send_event_request_expects_event_destination_target_by_name():
    """Test that event_destination_target can be set by its Python name and dumps as callback_url."""
    model = SendEventRequest(
        app_id="01EB37HMH1M6SV18ZNJMN108K1",
        recipient={"contact_id": "01EKA5J45DA8Y30K4DDX0A7Z6C"},
        event={"composing_event": {}},
        event_destination_target="https://my-server.com/events",
    )

    assert model.event_destination_target == "https://my-server.com/events"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["callback_url"] == "https://my-server.com/events"


def test_send_event_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = SendEventRequest(
        app_id="01EB37HMH1M6SV18ZNJMN108K1",
        recipient={"contact_id": "01EKA5J45DA8Y30K4DDX0A7Z6C"},
        event={"composing_event": {}},
    )

    assert model.event_destination_target is None
    assert model.channel_priority_order is None
    assert model.event_metadata is None
    assert model.queue is None


@pytest.mark.parametrize("missing", ["app_id", "recipient", "event"])
def test_send_event_request_expects_validation_error_for_missing_required(
    missing,
):
    """Test that app_id, recipient and event are required."""
    data = {
        "app_id": "01EB37HMH1M6SV18ZNJMN108K1",
        "recipient": {"contact_id": "01EKA5J45DA8Y30K4DDX0A7Z6C"},
        "event": {"composing_event": {}},
    }
    del data[missing]

    with pytest.raises(ValidationError):
        SendEventRequest(**data)
