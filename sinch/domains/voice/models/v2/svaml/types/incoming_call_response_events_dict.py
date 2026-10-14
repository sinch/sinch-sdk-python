from collections.abc import Sequence
from typing import TYPE_CHECKING, TypedDict

from typing_extensions import NotRequired

if TYPE_CHECKING:
    from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
        SvamlCommandDict,
    )


class IncomingCallResponseEventsDict(TypedDict):
    on_hangup: NotRequired[Sequence["SvamlCommandDict"]]
