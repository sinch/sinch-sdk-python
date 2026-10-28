from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.analysis_result import (
    AnalysisResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.machine_learning_image_recognition_result import (
    MachineLearningImageRecognitionResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.machine_learning_nlu_result import (
    MachineLearningNLUResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.machine_learning_pii_result import (
    MachineLearningPIIResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.machine_learning_sentiment_result import (
    MachineLearningSentimentResult,
)
from sinch.domains.conversation.models.v1.sinch_events.smart_conversations.offensive_analysis import (
    OffensiveAnalysis,
)


def test_analysis_result_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = AnalysisResult(
        ml_sentiment_result=[{"message": "Hi", "sentiment": "positive", "score": 0.5}],
        ml_nlu_result=[{"message": "Hi", "intent": "chitchat.greeting", "score": 0.5}],
        ml_image_recognition_result=[{"url": "https://example.com/image.png"}],
        ml_pii_result=[{"message": "Hi", "masked": "Hi"}],
        ml_offensive_analysis_result=[{"message": "Hi", "evaluation": "SAFE", "score": 0.5}],
    )

    assert isinstance(model.ml_sentiment_result[0], MachineLearningSentimentResult)
    assert model.ml_sentiment_result[0].sentiment == "positive"
    assert isinstance(model.ml_nlu_result[0], MachineLearningNLUResult)
    assert model.ml_nlu_result[0].intent == "chitchat.greeting"
    assert isinstance(
        model.ml_image_recognition_result[0], MachineLearningImageRecognitionResult
    )
    assert model.ml_image_recognition_result[0].url == "https://example.com/image.png"
    assert isinstance(model.ml_pii_result[0], MachineLearningPIIResult)
    assert model.ml_pii_result[0].masked == "Hi"
    assert isinstance(model.ml_offensive_analysis_result[0], OffensiveAnalysis)
    assert model.ml_offensive_analysis_result[0].evaluation == "SAFE"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["ml_sentiment_result"] == [
        {"message": "Hi", "sentiment": "positive", "score": 0.5}
    ]
    assert alias_dump["ml_nlu_result"] == [
        {"message": "Hi", "intent": "chitchat.greeting", "score": 0.5}
    ]
    assert alias_dump["ml_image_recognition_result"] == [
        {"url": "https://example.com/image.png"}
    ]
    assert alias_dump["ml_pii_result"] == [{"message": "Hi", "masked": "Hi"}]
    assert alias_dump["ml_offensive_analysis_result"] == [
        {"message": "Hi", "evaluation": "SAFE", "score": 0.5}
    ]


def test_analysis_result_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = AnalysisResult()

    assert model.ml_sentiment_result is None
    assert model.ml_nlu_result is None
    assert model.ml_image_recognition_result is None
    assert model.ml_pii_result is None
    assert model.ml_offensive_analysis_result is None
