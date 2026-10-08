from typing import List, Union, cast

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.helpers.v2.destinations import Destination
from sinch.domains.voice.models.v2.svaml.types import (
    AnswerCommandDict,
    BridgeCallCommandDict,
    DialCommandDict,
    HangupCommandDict,
    PauseCommandDict,
    SvamlCommandDict,
)
from sinch.domains.voice.models.v2.types import (
    BaseCallDestinationDict,
    CallDestinationDict,
    CallOriginDict,
)


class Calls:
    """Helpers to build the call control SVAML commands."""

    @staticmethod
    def answer() -> AnswerCommandDict:
        """
        Answers an inbound call leg. This is a non-blocking command — execution
        continues to the next command in the sequence immediately after the answer
        is initiated.

        :returns: The ``answer`` command.
        :rtype: AnswerCommandDict
        """
        return {"command": "answer"}

    @staticmethod
    def bridge_call(name: str) -> BridgeCallCommandDict:
        """
        Adds the current call to a bridge, enabling bidirectional audio
        communication with other calls in the same session. This is a non-blocking
        command — execution continues to the next command in the sequence
        immediately after the call joins the bridge.

        Bridges are created automatically when referenced by name. If a bridge with
        the specified name already exists, the call joins that bridge; otherwise, a
        new bridge is created.

        :param name: Name of the bridge to join. If no bridge with this name
            exists in the session, a new one is created automatically.
        :type name: str
        :returns: The ``bridgeCall`` command.
        :rtype: BridgeCallCommandDict
        """
        return {"command": "bridgeCall", "bridge_name": name}

    @staticmethod
    def dial(
        to: Union[str, BaseCallDestinationDict, CallDestinationDict],
        *,
        from_: UnsetOr[
            Union[str, BaseCallDestinationDict, CallOriginDict]
        ] = UNSET,
        name: UnsetOr[str] = UNSET,
        timeout_duration_seconds: UnsetOr[int] = UNSET,
        max_duration_seconds: UnsetOr[int] = UNSET,
        on_answer: UnsetOr[List[SvamlCommandDict]] = UNSET,
        on_busy: UnsetOr[List[SvamlCommandDict]] = UNSET,
        on_reject: UnsetOr[List[SvamlCommandDict]] = UNSET,
        on_timeout: UnsetOr[List[SvamlCommandDict]] = UNSET,
        on_hangup: UnsetOr[List[SvamlCommandDict]] = UNSET,
        on_failure: UnsetOr[List[SvamlCommandDict]] = UNSET,
    ) -> DialCommandDict:
        """
        Initiates a new outbound call leg within the current session.

        This is a non-blocking command — the next command in the sequence executes
        immediately while the call is being established in parallel. Call lifecycle
        events (answer, busy, reject, timeout, hangup, failure) are handled via the
        `events` property.

        The `from` and `to` endpoint types should ideally match. If they differ, the
        platform attempts to convert the `from` value to be compatible with the `to`
        type. For example, PSTN supports only E.164 phone numbers, so a SIP address
        such as `sip:46701234567@acme.se` can be converted to an E.164 number. If the
        `from` value cannot be converted, it defaults to null (anonymous).

        :param to: Call destination: a phone number in E.164 format,
            a SIP URI, a WebSocket endpoint for real-time audio
            streaming or the Voice Relay service for real-time
            speech-to-text and text-to-speech. A string is parsed with
            :meth:`Destination.of`.
        :type to: Union[str, BaseCallDestinationDict, CallDestinationDict]
        :param from_: Call origin: a phone number in E.164 format or
            a SIP URI. A string is parsed with :meth:`Destination.of`.
        :type from_: UnsetOr[Union[str, BaseCallDestinationDict, CallOriginDict]]
        :param name: Identifier for this call leg within the session. Must be
            unique across all active call legs in the session. Other commands (e.g.,
            `hangup`) can reference this name to target this specific leg.
        :type name: UnsetOr[str]
        :param timeout_duration_seconds: Maximum time in seconds to wait for the
            call to be answered. If the timeout expires without an answer, the
            `onTimeout` event is triggered.
        :type timeout_duration_seconds: UnsetOr[int]
        :param max_duration_seconds: Maximum duration of the call in seconds.
            The call is terminated automatically when this limit is reached.
        :type max_duration_seconds: UnsetOr[int]
        :param on_answer: SVAML commands to be executed when the call is answered.
        :type on_answer: UnsetOr[List[SvamlCommandDict]]
        :param on_busy: SVAML commands to be executed when the call is busy.
        :type on_busy: UnsetOr[List[SvamlCommandDict]]
        :param on_reject: SVAML commands to be executed when the call is rejected.
        :type on_reject: UnsetOr[List[SvamlCommandDict]]
        :param on_timeout: SVAML commands to be executed when the call is timed out.
        :type on_timeout: UnsetOr[List[SvamlCommandDict]]
        :param on_hangup: SVAML commands to be executed when the call is hung up.
        :type on_hangup: UnsetOr[List[SvamlCommandDict]]
        :param on_failure: SVAML commands to be executed when the call fails.
        :type on_failure: UnsetOr[List[SvamlCommandDict]]
        :returns: The ``dial`` command.
        :rtype: DialCommandDict
        """
        events = strip_unset(
            {
                "on_answer": on_answer,
                "on_busy": on_busy,
                "on_reject": on_reject,
                "on_timeout": on_timeout,
                "on_hangup": on_hangup,
                "on_failure": on_failure,
            }
        )
        return cast(
            DialCommandDict,
            strip_unset(
                {
                    "command": "dial",
                    "to": Destination.of(to) if isinstance(to, str) else to,
                    "from_": (
                        Destination.of(from_)
                        if isinstance(from_, str)
                        else from_
                    ),
                    "call_name": name,
                    "dial_timeout_duration_seconds": timeout_duration_seconds,
                    "max_call_duration_seconds": max_duration_seconds,
                    "events": events if events else UNSET,
                }
            ),
        )

    @staticmethod
    def hangup(name: UnsetOr[str] = UNSET) -> HangupCommandDict:
        """
        Ends a call leg. This is a non-blocking command — execution continues to the
        next command in the sequence even though the call has been ended. The
        `onHangup` event is triggered for the call leg that was ended.

        Any subsequent commands that target the ended call leg (such as `messages`
        or other media commands) are valid but will not be executed. Commands that
        operate independently — such as initiating a new call with `dial` — will
        execute normally. This makes it possible, for example, to end one call and
        immediately start another within the same sequence.

        :param name: Name of the call leg to end, as set by `callName` in the
            `dial` command. If omitted, the current call leg is ended.
        :type name: UnsetOr[str]
        :returns: The ``hangup`` command.
        :rtype: HangupCommandDict
        """
        return cast(
            HangupCommandDict,
            strip_unset({"command": "hangup", "call_name": name}),
        )

    @staticmethod
    def pause(duration_milliseconds: int) -> PauseCommandDict:
        """
        Delays execution of the next command in the sequence for a specified
        duration. This is a blocking command — no further commands execute until the
        pause completes.

        The pause does not affect call audio; the call remains connected and audio
        continues uninterrupted.

        :param duration_milliseconds: Duration of the pause in milliseconds.
        :type duration_milliseconds: int
        :returns: The ``pause`` command.
        :rtype: PauseCommandDict
        """
        return {
            "command": "pause",
            "duration_milliseconds": duration_milliseconds,
        }
