from typing import TYPE_CHECKING, List, TypedDict

from typing_extensions import NotRequired

if TYPE_CHECKING:
    from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
        SvamlCommandDict,
    )


class AmdEventsDict(TypedDict):
    on_human: NotRequired[List["SvamlCommandDict"]]
    on_machine: NotRequired[List["SvamlCommandDict"]]
    on_beep: NotRequired[List["SvamlCommandDict"]]
    on_unknown: NotRequired[List["SvamlCommandDict"]]
