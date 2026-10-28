from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.machine_learning_sentiment_result import (
    MachineLearningSentimentResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.sentiment_result import (
    SentimentResult,
)


def test_machine_learning_sentiment_result_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MachineLearningSentimentResult(
        message="I love Sinch",
        sentiment="positive",
        score=0.75,
        results=[
            {"sentiment": "negative", "score": 0.25},
            {"sentiment": "positive", "score": 0.75},
        ],
    )

    assert isinstance(model, SentimentResult)
    assert model.message == "I love Sinch"
    assert model.sentiment == "positive"
    assert model.score == 0.75
    assert len(model.results) == 2
    assert isinstance(model.results[0], SentimentResult)
    assert model.results[0].sentiment == "negative"
    assert model.results[1].score == 0.75

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["message"] == "I love Sinch"
    assert alias_dump["sentiment"] == "positive"
    assert alias_dump["score"] == 0.75
    assert alias_dump["results"] == [
        {"sentiment": "negative", "score": 0.25},
        {"sentiment": "positive", "score": 0.75},
    ]


def test_machine_learning_sentiment_result_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MachineLearningSentimentResult()

    assert model.message is None
    assert model.results is None
    assert model.sentiment is None
    assert model.score is None
