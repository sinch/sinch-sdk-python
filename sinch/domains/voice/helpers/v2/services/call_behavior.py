from collections.abc import Sequence
from typing import cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.models.v2.services.types import (
    EventDestinationCallBehaviorDict,
    NoneCallBehaviorDict,
    StaticCallBehaviorDict,
)
from sinch.domains.voice.models.v2.svaml.types import SvamlCommandDict


class CallBehavior:
    """Helpers to build the call behavior of a service."""

    @staticmethod
    def event_destination(
        url: str,
        *,
        fallback_url: UnsetOr[str] = UNSET,
    ) -> EventDestinationCallBehaviorDict:
        """
        Calls are handled dynamically by sending events to the configured URL.
        The backend responds with SVAML commands that control the call flow in
        real time.

        :param url: Event destination URL.
        :type url: str
        :param fallback_url: Fallback URL used when the primary
            URL fails. A failed request is re-sent to this URL immediately.
            After repeated consecutive failures of the primary URL, requests are
            sent only here until the primary URL recovers.
        :type fallback_url: UnsetOr[str]
        :returns: The ``EVENT_DESTINATION`` call behavior.
        :rtype: EventDestinationCallBehaviorDict
        """
        return cast(
            EventDestinationCallBehaviorDict,
            {
                "type": "EVENT_DESTINATION",
                "event_destination": strip_unset(
                    {"url": url, "fallback_url": fallback_url}
                ),
            },
        )

    @staticmethod
    def none() -> NoneCallBehaviorDict:
        """
        No call behavior is configured for the service. Incoming calls will not
        be handled and outbound calls can still be initiated via the API.

        :returns: The ``NONE`` call behavior.
        :rtype: NoneCallBehaviorDict
        """
        return {"type": "NONE"}

    @staticmethod
    def static(
        commands: Sequence[SvamlCommandDict],
        *,
        name: UnsetOr[str] = UNSET,
        on_hangup: UnsetOr[Sequence[SvamlCommandDict]] = UNSET,
    ) -> StaticCallBehaviorDict:
        """
        Calls are handled using a predefined static SVAML script. The commands
        are executed for every call on this service, without any backend
        involvement.

        :param commands: An ordered list of SVAML v2 (Sinch Voice Application
            Markup Language) commands that describe a call flow. Commands are
            executed sequentially in the order they are defined.
        :type commands: Sequence[SvamlCommandDict]
        :param name: Name of the call. Must be 1-32 characters. Regex
            pattern: `^\\S+$`
        :type name: UnsetOr[str]
        :param on_hangup: SVAML commands to be executed when the call is hung
            up.
        :type on_hangup: UnsetOr[Sequence[SvamlCommandDict]]
        :returns: The ``STATIC`` call behavior.
        :rtype: StaticCallBehaviorDict
        """
        events = strip_unset({"on_hangup": on_hangup})
        return cast(
            StaticCallBehaviorDict,
            {
                "type": "STATIC",
                "static": strip_unset(
                    {
                        "commands": commands,
                        "call_name": name,
                        "events": events if events else UNSET,
                    }
                ),
            },
        )
