from collections.abc import Sequence
from typing import TYPE_CHECKING, TypedDict

from typing_extensions import NotRequired

if TYPE_CHECKING:
    from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
        SvamlCommandDict,
    )


class CallEventsDict(TypedDict):
    on_answer: NotRequired[Sequence["SvamlCommandDict"]]
    on_busy: NotRequired[Sequence["SvamlCommandDict"]]
    on_reject: NotRequired[Sequence["SvamlCommandDict"]]
    on_timeout: NotRequired[Sequence["SvamlCommandDict"]]
    on_hangup: NotRequired[Sequence["SvamlCommandDict"]]
    on_failure: NotRequired[Sequence["SvamlCommandDict"]]
