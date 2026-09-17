from typing import List

from typing_extensions import TypedDict

from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
    SvamlCommandDict,
)


class SvamlInputDict(TypedDict):
    commands: List[SvamlCommandDict]
