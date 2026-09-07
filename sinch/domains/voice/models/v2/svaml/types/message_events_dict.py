from typing import TYPE_CHECKING, List, TypedDict

from typing_extensions import NotRequired

if TYPE_CHECKING:
    from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
        SvamlCommandDict,
    )


class MessageEventsDict(TypedDict):
    on_finish: NotRequired[List["SvamlCommandDict"]]
