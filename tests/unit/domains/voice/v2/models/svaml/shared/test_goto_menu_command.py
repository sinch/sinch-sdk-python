import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.goto_menu_command import (
    GotoMenuCommand,
)


def test_goto_menu_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = GotoMenuCommand(command="gotoMenu", menu_name="main")

    assert model.command == "gotoMenu"
    assert model.menu_name == "main"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["menuName"] == "main"


def test_goto_menu_command_expects_validation_error_for_missing_required():
    """Test that menu_name is required."""
    with pytest.raises(ValidationError):
        GotoMenuCommand(command="gotoMenu")
