from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_field_classification import (
    DocumentFieldClassification,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_image_classification import (
    DocumentImageClassification,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.machine_learning_image_recognition_result import (
    MachineLearningImageRecognitionResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.optical_character_recognition import (
    OpticalCharacterRecognition,
)


def test_machine_learning_image_recognition_result_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MachineLearningImageRecognitionResult(
        url="https://example.com/passport.png",
        document_image_classification={"doc_type": "passport", "confidence": 0.5},
        optical_character_recognition={"result": [{"data": ["JOHN"]}]},
        document_field_classification={"result": [{"first_name": {"data": ["JOHN"]}}]},
    )

    assert model.url == "https://example.com/passport.png"
    assert isinstance(model.document_image_classification, DocumentImageClassification)
    assert model.document_image_classification.doc_type == "passport"
    assert isinstance(model.optical_character_recognition, OpticalCharacterRecognition)
    assert model.optical_character_recognition.result[0].data == ["JOHN"]
    assert isinstance(model.document_field_classification, DocumentFieldClassification)
    assert model.document_field_classification.result[0]["first_name"].data == ["JOHN"]

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["url"] == "https://example.com/passport.png"
    assert alias_dump["document_image_classification"] == {
        "doc_type": "passport",
        "confidence": 0.5,
    }
    assert alias_dump["optical_character_recognition"] == {
        "result": [{"data": ["JOHN"]}]
    }
    assert alias_dump["document_field_classification"] == {
        "result": [{"first_name": {"data": ["JOHN"]}}]
    }


def test_machine_learning_image_recognition_result_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MachineLearningImageRecognitionResult()

    assert model.url is None
    assert model.document_image_classification is None
    assert model.optical_character_recognition is None
    assert model.document_field_classification is None
