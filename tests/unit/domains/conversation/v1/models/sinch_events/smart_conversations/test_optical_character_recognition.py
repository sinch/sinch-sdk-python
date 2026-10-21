from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.optical_character_recognition import (
    OpticalCharacterRecognition,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.optical_character_recognition_data import (
    OpticalCharacterRecognitionData,
)


def test_optical_character_recognition_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = OpticalCharacterRecognition(
        result=[{"data": ["JOHN", "SMITH"]}, {"data": ["123456"]}]
    )

    assert len(model.result) == 2
    assert isinstance(model.result[0], OpticalCharacterRecognitionData)
    assert model.result[0].data == ["JOHN", "SMITH"]
    assert model.result[1].data == ["123456"]

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["result"] == [
        {"data": ["JOHN", "SMITH"]},
        {"data": ["123456"]},
    ]


def test_optical_character_recognition_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = OpticalCharacterRecognition()

    assert model.result is None
