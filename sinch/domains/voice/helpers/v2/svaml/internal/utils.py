from collections.abc import Mapping, Sequence
from typing import Union, cast

from sinch.core.sentinel import UnsetOr
from sinch.domains.voice.models.v2.svaml.types import SvamlCommandDict


def as_commands(
    commands: UnsetOr[Union[SvamlCommandDict, Sequence[SvamlCommandDict]]],
) -> UnsetOr[Sequence[SvamlCommandDict]]:
    """Wraps a single command in a list; sequences and UNSET are kept."""
    if isinstance(commands, Mapping):
        return [cast(SvamlCommandDict, commands)]
    return commands
