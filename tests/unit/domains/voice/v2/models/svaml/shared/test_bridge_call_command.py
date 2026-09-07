import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.bridge_call_command import (
    BridgeCallCommand,
)


def test_bridge_call_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = BridgeCallCommand(command="bridgeCall", bridge_name="my_bridge")

    assert model.command == "bridgeCall"
    assert model.bridge_name == "my_bridge"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["bridgeName"] == "my_bridge"


def test_bridge_call_command_expects_validation_error_for_missing_required():
    """Test that bridge_name is required."""
    with pytest.raises(ValidationError):
        BridgeCallCommand(command="bridgeCall")
