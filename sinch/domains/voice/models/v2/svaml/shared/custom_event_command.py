from typing import Literal, Optional

from pydantic import Field, StrictStr, field_serializer, model_validator

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)

_WIRE_COMMAND_VALUE = "webhook"
_SDK_COMMAND_VALUE = "customEvent"


class CustomEventCommand(BaseModelConfiguration):
    command: Literal[_SDK_COMMAND_VALUE] = Field(
        default=_SDK_COMMAND_VALUE,
        description="Command to trigger a mid-call Custom Event",
    )
    custom_event_name: StrictStr = Field(
        default=...,
        alias="webhookName",
        description='Name for this Custom Event. When triggered, the Sinch Event request\'s `event` property will contain this name prepended with `call.customEvent.`.\n\nFor example, if `custom_event_name` is set to `"my.custom.event"`, the event will be delivered as `"call.customEvent.my.custom.event"`.',
    )
    url: StrictStr = Field(
        default=...,
        description="URL of the endpoint to send the mid-call Sinch Event to.",
    )
    fallback_url: Optional[StrictStr] = Field(
        default=None,
        alias="fallbackUrl",
        description="Fallback URL used when the primary URL fails.\n\nA failed request is re-sent to this URL immediately. After repeated consecutive failures of the primary URL, requests are sent only here until the primary URL recovers.\n\nSee *Timeouts and failover* in the **Webhooks** section for the authoritative algorithm.",
    )

    @model_validator(mode="before")
    @classmethod
    def _accept_wire_command_value(cls, data):
        if (
            isinstance(data, dict)
            and data.get("command") == _WIRE_COMMAND_VALUE
        ):
            data = {**data, "command": _SDK_COMMAND_VALUE}
        return data

    @field_serializer("command")
    def _serialize_command(self, _value: str) -> str:
        return _WIRE_COMMAND_VALUE
