from typing import Optional

from pydantic import Field, model_validator

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.internal.utils.helpers import (
    rename_wire_event_prefix,
)
from sinch.domains.voice.models.v2.shared.call import Call
from sinch.domains.voice.models.v2.sinch_events.menu_input import MenuInput
from sinch.domains.voice.models.v2.sinch_events.event_type import (
    EventType,
)


class VoiceSinchEventRequest(BaseModelConfiguration):
    event: EventType = Field(
        default=...,
        description="""Identifies the type of call event that triggered this sinch event notification.

Call-related sinch events always start with `call.` followed by the type of event that triggered them. Events triggered by the `customEvent` SVAML command are dynamic and follow the pattern `call.customEvent.<customEventName>`.""",
    )
    call: Call = Field(
        default=...,
        description="The current state of the call at the time the event was triggered.",
    )
    menu: Optional[MenuInput] = Field(
        default=None,
        description="""Information about the menu interaction that triggered the sinch event, including the menu name and the input sequence received from the user.

This property is also included for sinch events triggered by the `customEvent` command within a menu context.""",
    )

    @model_validator(mode="before")
    @classmethod
    def _rename_wire_event_prefix(cls, data):
        return rename_wire_event_prefix(data)
