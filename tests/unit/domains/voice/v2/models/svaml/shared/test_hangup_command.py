from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)


def test_hangup_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = HangupCommand(command="hangup", call_name="origin")

    assert model.command == "hangup"
    assert model.call_name == "origin"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["callName"] == "origin"


def test_hangup_command_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = HangupCommand(command="hangup")

    assert model.call_name is None
