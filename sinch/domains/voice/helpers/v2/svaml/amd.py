from typing import List, cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.models.v2.svaml.types import (
    AmdCommandDict,
    SvamlCommandDict,
)


class Amd:
    """Helpers to build the Answering Machine Detection SVAML commands."""

    @staticmethod
    def activate(
        *,
        on_human: UnsetOr[List[SvamlCommandDict]] = UNSET,
        on_machine: UnsetOr[List[SvamlCommandDict]] = UNSET,
        on_beep: UnsetOr[List[SvamlCommandDict]] = UNSET,
        on_unknown: UnsetOr[List[SvamlCommandDict]] = UNSET,
    ) -> AmdCommandDict:
        """
        AMD (Answering Machine Detection) command to detect what answered the
        call. Possible outcomes are: human, machine, beep, or unknown.

        This is a non-blocking command — the next command in the sequence
        executes immediately while detection runs in parallel. Results are
        delivered via events, which defines different call
        flows depending on whether a human, machine, beep, or unknown entity
        answers the call.

        :param on_human: SVAML commands to be executed when a human is
            detected.
        :type on_human: UnsetOr[List[SvamlCommandDict]]
        :param on_machine: SVAML commands to be executed when a machine is
            detected.
        :type on_machine: UnsetOr[List[SvamlCommandDict]]
        :param on_beep: SVAML commands to be executed when a beep is detected.
        :type on_beep: UnsetOr[List[SvamlCommandDict]]
        :param on_unknown: SVAML commands to be executed when an unknown event
            is detected.
        :type on_unknown: UnsetOr[List[SvamlCommandDict]]
        :returns: The ``amd`` command.
        :rtype: AmdCommandDict
        """
        events = strip_unset(
            {
                "on_human": on_human,
                "on_machine": on_machine,
                "on_beep": on_beep,
                "on_unknown": on_unknown,
            }
        )
        return cast(
            AmdCommandDict,
            strip_unset(
                {"command": "amd", "events": events if events else UNSET}
            ),
        )
