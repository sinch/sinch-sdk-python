from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.optical_character_recognition_data import (
    OpticalCharacterRecognitionData,
)


def test_optical_character_recognition_data_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = OpticalCharacterRecognitionData(data=["JOHN", "SMITH"])

    assert model.data == ["JOHN", "SMITH"]

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["data"] == ["JOHN", "SMITH"]


def test_optical_character_recognition_data_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = OpticalCharacterRecognitionData()

    assert model.data is None
