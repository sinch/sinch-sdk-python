from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_image_classification import (
    DocumentImageClassification,
)


def test_document_image_classification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DocumentImageClassification(doc_type="passport", confidence=0.5)

    assert model.doc_type == "passport"
    assert model.confidence == 0.5

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["doc_type"] == "passport"
    assert alias_dump["confidence"] == 0.5


def test_document_image_classification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = DocumentImageClassification()

    assert model.doc_type is None
    assert model.confidence is None
