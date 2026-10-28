from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_field_data import (
    DocumentFieldData,
)


def test_document_field_data_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DocumentFieldData(data=["JOHN"])

    assert model.data == ["JOHN"]

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["data"] == ["JOHN"]


def test_document_field_data_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = DocumentFieldData()

    assert model.data is None
