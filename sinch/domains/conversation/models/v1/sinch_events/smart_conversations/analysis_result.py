from typing import Optional

from pydantic import Field, conlist

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
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


class AnalysisResult(SinchEvent):
    """The analysis provided by the Smart Conversations machine learning engine(s). The contents of the object are determined by the functionalities that are enabled for your solution."""

    ml_sentiment_result: Optional[conlist(MachineLearningSentimentResult)] = (
        Field(
            default=None,
            description="An array that contains the analyses of the sentiments of the corresponding messages.",
        )
    )
    ml_nlu_result: Optional[conlist(MachineLearningNLUResult)] = Field(
        default=None,
        description="An array that contains the analyses of the intentions of, and entities within, the corresponding messages.",
    )
    ml_image_recognition_result: Optional[
        conlist(MachineLearningImageRecognitionResult)
    ] = Field(
        default=None,
        description="An array that contains the image recognition analyses of the images identified in the corresponding messages.",
    )
    ml_pii_result: Optional[conlist(MachineLearningPIIResult)] = Field(
        default=None,
        description="An array that contains the PII analysis of the corresponding messages.",
    )
    ml_offensive_analysis_result: Optional[conlist(OffensiveAnalysis)] = Field(
        default=None,
        description="An array that contains the analyses of the offenses of the corresponding messages.",
    )
