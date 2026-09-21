import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.dial_command import DialCommand

TO = {"type": "PHONE", "phone": {"number": "+15559876543"}}
FROM = {"type": "PHONE", "phone": {"number": "+15551234567"}}


def test_dial_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DialCommand(
        command="dial",
        call_name="origin",
        from_=FROM,
        to=TO,
        dial_timeout_duration_seconds=30,
        max_call_duration_seconds=3600,
        events={"on_hangup": [{"command": "hangup"}]},
    )

    assert model.command == "dial"
    assert model.call_name == "origin"
    assert model.from_.phone.number == "+15551234567"
    assert model.to.phone.number == "+15559876543"
    assert model.dial_timeout_duration_seconds == 30
    assert model.max_call_duration_seconds == 3600
    assert model.events.on_hangup[0].command == "hangup"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["callName"] == "origin"
    assert alias_dump["from"] == FROM
    assert alias_dump["dialTimeoutDurationSeconds"] == 30
    assert alias_dump["maxCallDurationSeconds"] == 3600


def test_dial_command_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = DialCommand(command="dial", to=TO)

    assert model.call_name is None
    assert model.from_ is None
    assert model.dial_timeout_duration_seconds is None
    assert model.max_call_duration_seconds is None
    assert model.events is None


def test_dial_command_expects_validation_error_for_missing_required():
    """Test that to is required."""
    with pytest.raises(ValidationError):
        DialCommand(command="dial")
