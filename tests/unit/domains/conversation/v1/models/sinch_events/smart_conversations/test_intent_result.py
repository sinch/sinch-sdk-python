from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.intent_result import (
    IntentResult,
)


def test_intent_result_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = IntentResult(intent="chitchat.thank_you", score=0.5)

    assert model.intent == "chitchat.thank_you"
    assert model.score == 0.5

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["intent"] == "chitchat.thank_you"
    assert alias_dump["score"] == 0.5


def test_intent_result_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = IntentResult()

    assert model.intent is None
    assert model.score is None
