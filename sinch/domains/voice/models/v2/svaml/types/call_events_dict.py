from typing import TYPE_CHECKING, List, TypedDict

from typing_extensions import NotRequired

if TYPE_CHECKING:
    from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
        SvamlCommandDict,
    )


class CallEventsDict(TypedDict):
    on_answer: NotRequired[List["SvamlCommandDict"]]
    on_busy: NotRequired[List["SvamlCommandDict"]]
    on_reject: NotRequired[List["SvamlCommandDict"]]
    on_timeout: NotRequired[List["SvamlCommandDict"]]
    on_hangup: NotRequired[List["SvamlCommandDict"]]
    on_failure: NotRequired[List["SvamlCommandDict"]]
