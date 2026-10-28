from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.offensive_analysis import (
    OffensiveAnalysis,
)


def test_offensive_analysis_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = OffensiveAnalysis(
        message="Hello",
        url="https://example.com/image.png",
        evaluation="UNSAFE",
        score=0.25,
    )

    assert model.message == "Hello"
    assert model.url == "https://example.com/image.png"
    assert model.evaluation == "UNSAFE"
    assert model.score == 0.25

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["message"] == "Hello"
    assert alias_dump["url"] == "https://example.com/image.png"
    assert alias_dump["evaluation"] == "UNSAFE"
    assert alias_dump["score"] == 0.25


def test_offensive_analysis_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = OffensiveAnalysis()

    assert model.message is None
    assert model.url is None
    assert model.evaluation is None
    assert model.score is None


def test_offensive_analysis_expects_unknown_evaluation_accepted():
    """Test that an unknown evaluation value is accepted through the StrictStr fallback."""
    model = OffensiveAnalysis(evaluation="UNKNOWN")

    assert model.evaluation == "UNKNOWN"
