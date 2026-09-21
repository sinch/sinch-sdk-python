import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.sinch_events.menu_input import MenuInput


def test_menu_input_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MenuInput(menu_name="main", input="1")

    assert model.menu_name == "main"
    assert model.input == "1"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["menuName"] == "main"
    assert alias_dump["input"] == "1"


def test_menu_input_expects_validation_error_for_missing_required():
    """Test that menu_name and input are required."""
    with pytest.raises(ValidationError):
        MenuInput()
