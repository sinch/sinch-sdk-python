from typing import Union

from sinch.domains.voice.models.v2.svaml.types.amd_command_dict import (
    AmdCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.answer_command_dict import (
    AnswerCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.bridge_call_command_dict import (
    BridgeCallCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.dial_command_dict import (
    DialCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.goto_menu_command_dict import (
    GotoMenuCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.hangup_command_dict import (
    HangupCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.menu_command_dict import (
    MenuCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.messages_command_dict import (
    MessagesCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.pause_command_dict import (
    PauseCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.custom_event_command_dict import (
    CustomEventCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.start_recording_command_dict import (
    StartRecordingCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.stop_messages_command_dict import (
    StopMessagesCommandDict,
)
from sinch.domains.voice.models.v2.svaml.types.stop_recording_command_dict import (
    StopRecordingCommandDict,
)

SvamlCommandDict = Union[
    AmdCommandDict,
    DialCommandDict,
    MessagesCommandDict,
    StopMessagesCommandDict,
    CustomEventCommandDict,
    HangupCommandDict,
    AnswerCommandDict,
    PauseCommandDict,
    StartRecordingCommandDict,
    StopRecordingCommandDict,
    BridgeCallCommandDict,
    MenuCommandDict,
    GotoMenuCommandDict,
]
