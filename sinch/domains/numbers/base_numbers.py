from typing import TypedDict, Literal, Union, Annotated
from typing_extensions import NotRequired
from pydantic import Field
from sinch.domains.numbers.models.numbers import NumberSearchPatternTypeValues


class SmsConfigurationDict(TypedDict):
    service_plan_id: str
    campaign_id: NotRequired[str]


class VoiceConfigurationDictRTC(TypedDict):
    type: Literal["RTC"]
    app_id: NotRequired[str]


class VoiceConfigurationDictEST(TypedDict):
    type: Literal["EST"]
    trunk_id: NotRequired[str]


class VoiceConfigurationDictFAX(TypedDict):
    type: Literal["FAX"]
    service_id: NotRequired[str]


class VoiceConfigurationDictCustom(TypedDict):
    type: str


class NumberPatternDict(TypedDict):
    pattern: NotRequired[str]
    search_pattern: NotRequired[NumberSearchPatternTypeValues]


VoiceConfigurationDictType = Annotated[
    Union[VoiceConfigurationDictFAX, VoiceConfigurationDictRTC,
          VoiceConfigurationDictEST, VoiceConfigurationDictCustom],
    Field(discriminator="type")
]


class BaseNumbers:
    """Base class for handling Sinch Number operations."""

    def __init__(self, sinch):
        self._sinch = sinch

    def _request(self, endpoint_class, request_data):
        """
        A helper method to make requests to endpoints.

        Args:
            endpoint_class: The endpoint class to call.
            request_data: The request data to pass to the endpoint.

        Returns:
            The response from the Sinch transport request.
        """
        return self._sinch.configuration.transport.request(
            endpoint_class(
                project_id=self._sinch.configuration.project_id,
                request_data=request_data
            )
        )
