from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.sentiment_result import (
    SentimentResult,
)


def test_sentiment_result_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SentimentResult(sentiment="positive", score=0.75)

    assert model.sentiment == "positive"
    assert model.score == 0.75

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["sentiment"] == "positive"
    assert alias_dump["score"] == 0.75


def test_sentiment_result_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = SentimentResult()

    assert model.sentiment is None
    assert model.score is None


def test_sentiment_result_expects_unknown_sentiment_accepted():
    """Test that an unknown sentiment value is accepted through the StrictStr fallback."""
    model = SentimentResult(sentiment="ambivalent")

    assert model.sentiment == "ambivalent"


def test_sentiment_result_expects_integer_score_accepted():
    """Test that an integer score is accepted."""
    model = SentimentResult(score=1)

    assert model.score == 1
