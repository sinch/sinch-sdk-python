from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from sinch.domains.voice.models.v2.svaml.shared.amd_command import AmdCommand
from sinch.domains.voice.models.v2.svaml.shared.amd_events import AmdEvents
from sinch.domains.voice.models.v2.svaml.shared.answer_command import (
    AnswerCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.bridge_call_command import (
    BridgeCallCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.call_events import CallEvents
from sinch.domains.voice.models.v2.svaml.shared.dial_command import DialCommand
from sinch.domains.voice.models.v2.svaml.shared.goto_menu_command import (
    GotoMenuCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.menu_command import MenuCommand
from sinch.domains.voice.models.v2.svaml.shared.menu_item import MenuItem
from sinch.domains.voice.models.v2.svaml.shared.message_events import (
    MessageEvents,
)
from sinch.domains.voice.models.v2.svaml.shared.messages_command import (
    MessagesCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.pause_command import (
    PauseCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.recording_events import (
    RecordingEvents,
)
from sinch.domains.voice.models.v2.svaml.shared.custom_event_command import (
    CustomEventCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.start_recording_command import (
    StartRecordingCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.stop_messages_command import (
    StopMessagesCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.stop_recording_command import (
    StopRecordingCommand,
)

SvamlCommand = Annotated[
    Union[
        AmdCommand,
        DialCommand,
        MessagesCommand,
        StopMessagesCommand,
        CustomEventCommand,
        HangupCommand,
        AnswerCommand,
        PauseCommand,
        StartRecordingCommand,
        StopRecordingCommand,
        BridgeCallCommand,
        MenuCommand,
        GotoMenuCommand,
    ],
    Field(discriminator="command"),
]

# Each of these models lives in its own module and declares a
# `conlist("SvamlCommand")` field to describe nested SVAML commands.
# "SvamlCommand" is a forward reference that can't
# be resolved from those modules'. Instead, we rebuild them
# here, passing it explicitly via `_types_namespace`.
_namespace = {"SvamlCommand": SvamlCommand}
AmdEvents.model_rebuild(_types_namespace=_namespace)
CallEvents.model_rebuild(_types_namespace=_namespace)
MessageEvents.model_rebuild(_types_namespace=_namespace)
RecordingEvents.model_rebuild(_types_namespace=_namespace)
MenuItem.model_rebuild(_types_namespace=_namespace)
