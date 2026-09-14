import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.menu_command import MenuCommand
from sinch.domains.voice.models.v2.svaml.shared.menu_item import MenuItem


def test_menu_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MenuCommand(command="menu", start_menu="main", menus={"main": {}})

    assert model.command == "menu"
    assert model.start_menu == "main"
    assert isinstance(model.menus["main"], MenuItem)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["startMenu"] == "main"


def test_menu_command_expects_validation_error_for_missing_required():
    """Test that start_menu and menus are required."""
    with pytest.raises(ValidationError):
        MenuCommand(command="menu")
