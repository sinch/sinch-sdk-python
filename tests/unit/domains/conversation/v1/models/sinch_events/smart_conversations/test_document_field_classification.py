from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_field_classification import (
    DocumentFieldClassification,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.document_field_data import (
    DocumentFieldData,
)


def test_document_field_classification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DocumentFieldClassification(
        result=[
            {"first_name": {"data": ["JOHN"]}, "last_name": {"data": ["SMITH"]}},
            {"document_number": {"data": ["123456"]}},
        ]
    )

    assert len(model.result) == 2
    assert isinstance(model.result[0]["first_name"], DocumentFieldData)
    assert model.result[0]["first_name"].data == ["JOHN"]
    assert model.result[0]["last_name"].data == ["SMITH"]
    assert model.result[1]["document_number"].data == ["123456"]

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["result"] == [
        {"first_name": {"data": ["JOHN"]}, "last_name": {"data": ["SMITH"]}},
        {"document_number": {"data": ["123456"]}},
    ]


def test_document_field_classification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = DocumentFieldClassification()

    assert model.result is None
