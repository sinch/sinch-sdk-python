from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.intent_result import (
    IntentResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.machine_learning_nlu_result import (
    MachineLearningNLUResult,
)


def test_machine_learning_nlu_result_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MachineLearningNLUResult(
        message="Thank you",
        intent="chitchat.thank_you",
        score=0.5,
        results=[
            {"intent": "chitchat.thank_you", "score": 0.5},
            {"intent": "chitchat.bye", "score": 0.25},
        ],
    )

    assert isinstance(model, IntentResult)
    assert model.message == "Thank you"
    assert model.intent == "chitchat.thank_you"
    assert model.score == 0.5
    assert len(model.results) == 2
    assert isinstance(model.results[0], IntentResult)
    assert model.results[1].intent == "chitchat.bye"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["message"] == "Thank you"
    assert alias_dump["intent"] == "chitchat.thank_you"
    assert alias_dump["score"] == 0.5
    assert alias_dump["results"] == [
        {"intent": "chitchat.thank_you", "score": 0.5},
        {"intent": "chitchat.bye", "score": 0.25},
    ]


def test_machine_learning_nlu_result_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MachineLearningNLUResult()

    assert model.message is None
    assert model.results is None
    assert model.intent is None
    assert model.score is None
