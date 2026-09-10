from typing import Literal, Union

from pydantic import StrictStr

EventType = Union[
    Literal[
        "call.incoming",
        "call.answered",
        "call.busy",
        "call.rejected",
        "call.timeout",
        "call.hangup",
        "call.failed",
        "call.amd.human",
        "call.amd.machine",
        "call.amd.beep",
        "call.amd.unknown",
        "call.message.finished",
        "call.recording.finished",
        "call.recording.failed",
        "call.menu",
    ],
    StrictStr,
]
