from typing import cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.models.v2.svaml.types import CustomEventCommandDict


class CustomEvents:
    """Helpers to build the custom event SVAML commands."""

    @staticmethod
    def trigger(
        name: str,
        url: str,
        *,
        fallback_url: UnsetOr[str] = UNSET,
    ) -> CustomEventCommandDict:
        r"""
        Triggers a mid-call event to the application backend, allowing it to
        return a new set of SVAML commands that control the remainder of the
        call flow.

        This is a blocking command — execution pauses until a response is
        received from the event destination. The next command in the sequence
        runs only after the backend responds. Event requests use a 5-second
        timeout. If ``fallback_url`` is provided, a failed request is re-sent
        to it.

        :param name: Name for this custom event, between 1 and 64 characters,
            matching ``^\S+$``. When triggered, the event request's ``event``
            property contains this name prepended with ``call.customEvent.``.
        :type name: str
        :param url: URL of the event destination to send the mid-call event
            to.
        :type url: str
        :param fallback_url: Fallback URL used when the primary URL fails. A
            failed request is re-sent to this URL immediately. After repeated
            consecutive failures of the primary URL, requests are sent only
            here until the primary URL recovers.
        :type fallback_url: UnsetOr[str]
        :returns: The ``customEvent`` command.
        :rtype: CustomEventCommandDict
        """
        return cast(
            CustomEventCommandDict,
            strip_unset(
                {
                    "command": "customEvent",
                    "custom_event_name": name,
                    "url": url,
                    "fallback_url": fallback_url,
                }
            ),
        )
