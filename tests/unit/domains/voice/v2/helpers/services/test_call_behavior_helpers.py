from sinch.domains.voice.helpers.v2.services import CallBehavior
from sinch.domains.voice.helpers.v2.svaml import Calls


def test_event_destination_expects_all_fields():
    """Test that event_destination builds the behavior with all its fields."""
    behavior = CallBehavior.event_destination(
        "https://example.com/webhook",
        fallback_url="https://example.com/fallback",
    )

    assert behavior == {
        "type": "EVENT_DESTINATION",
        "event_destination": {
            "url": "https://example.com/webhook",
            "fallback_url": "https://example.com/fallback",
        },
    }


def test_event_destination_expects_optionals_omitted_when_not_provided():
    """Test that an omitted fallback_url is not included."""
    assert CallBehavior.event_destination("https://example.com/webhook") == {
        "type": "EVENT_DESTINATION",
        "event_destination": {"url": "https://example.com/webhook"},
    }


def test_none_expects_none_behavior():
    """Test that none builds the behavior."""
    assert CallBehavior.none() == {"type": "NONE"}


def test_static_expects_all_fields():
    """Test that static builds the behavior with all its fields."""
    behavior = CallBehavior.static(
        [Calls.answer(), Calls.hangup()],
        name="incoming",
        on_hangup=[Calls.hangup("destination")],
    )

    assert behavior == {
        "type": "STATIC",
        "static": {
            "commands": [{"command": "answer"}, {"command": "hangup"}],
            "call_name": "incoming",
            "events": {
                "on_hangup": [
                    {"command": "hangup", "call_name": "destination"}
                ]
            },
        },
    }


def test_static_expects_optionals_omitted_when_not_provided():
    """Test that omitted optionals, including events, are not included."""
    assert CallBehavior.static([Calls.answer()]) == {
        "type": "STATIC",
        "static": {"commands": [{"command": "answer"}]},
    }


def test_static_expects_empty_handler_kept():
    """Test that an explicit empty handler list is kept, so events is sent."""
    behavior = CallBehavior.static([Calls.answer()], on_hangup=[])
    assert behavior["static"]["events"] == {"on_hangup": []}


def test_static_expects_single_command_handler_wrapped():
    """Test that a handler given as a single command is sent as a list."""
    behavior = CallBehavior.static(Calls.answer(), on_hangup=Calls.hangup())
    assert behavior["static"]["events"] == {
        "on_hangup": [{"command": "hangup"}]
    }
