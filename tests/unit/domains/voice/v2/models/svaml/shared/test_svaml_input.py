from sinch.domains.voice.models.v2.svaml.shared.incoming_call_response_events import (
    IncomingCallResponseEvents,
)
from sinch.domains.voice.models.v2.svaml.shared.svaml_input import SvamlInput


def test_svaml_input_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SvamlInput(
        commands=[{"command": "hangup"}],
        call_name="incoming",
        events={"on_hangup": [{"command": "hangup"}]},
    )

    assert model.commands[0].command == "hangup"
    assert model.call_name == "incoming"
    assert isinstance(model.events, IncomingCallResponseEvents)
    assert model.events.on_hangup[0].command == "hangup"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["commands"][0]["command"] == "hangup"
    assert alias_dump["callName"] == "incoming"
    assert alias_dump["events"]["onHangup"] == [{"command": "hangup"}]


def test_svaml_input_expects_optionals_default_to_none():
    """Test that call_name and events default to None."""
    model = SvamlInput(commands=[{"command": "hangup"}])

    assert model.call_name is None
    assert model.events is None
