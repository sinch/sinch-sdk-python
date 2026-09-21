import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.menu_prompt import MenuPrompt

SAY_MESSAGE = {"type": "SAY", "say": {"text": "Hello", "voice_name": "Emma"}}


def test_menu_prompt_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MenuPrompt(allow_barge_in=True, messages=[SAY_MESSAGE])

    assert model.allow_barge_in is True
    assert model.messages[0].say.text == "Hello"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["allowBargeIn"] is True


def test_menu_prompt_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MenuPrompt(messages=[SAY_MESSAGE])

    assert model.allow_barge_in is None


def test_menu_prompt_expects_validation_error_for_missing_required():
    """Test that messages is required."""
    with pytest.raises(ValidationError):
        MenuPrompt()
