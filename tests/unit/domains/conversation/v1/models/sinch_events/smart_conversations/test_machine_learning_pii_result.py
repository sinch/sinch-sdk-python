from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.machine_learning_pii_result import (
    MachineLearningPIIResult,
)


def test_machine_learning_pii_result_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MachineLearningPIIResult(
        message="My name is Jane", masked="My name is {PERSON}"
    )

    assert model.message == "My name is Jane"
    assert model.masked == "My name is {PERSON}"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["message"] == "My name is Jane"
    assert alias_dump["masked"] == "My name is {PERSON}"


def test_machine_learning_pii_result_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MachineLearningPIIResult()

    assert model.message is None
    assert model.masked is None
