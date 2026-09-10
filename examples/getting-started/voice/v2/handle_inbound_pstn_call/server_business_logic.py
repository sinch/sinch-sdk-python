"""
On inbound PSTN call (call.incoming), answer, play a greeting, then dial an agent
number and bridge the two legs together.
"""

from sinch.domains.voice.api.v2.sinch_events import SinchEvents
from sinch.domains.voice.models.v2.shared.phone import Phone
from sinch.domains.voice.models.v2.sinch_events.voice_sinch_event_request import (
    VoiceSinchEventRequest,
)
from sinch.domains.voice.models.v2.sinch_events.voice_sinch_event_response import (
    VoiceSinchEventResponse,
)


def handle_voice_event(
    event: VoiceSinchEventRequest,
    logger,
    sinch_events_service: SinchEvents,
    sinch_number: str,
    destination_number: str,
) -> VoiceSinchEventResponse:
    """Sinch Event entry: handle only call.incoming; ignore everything else."""
    if event.event == "call.incoming":
        call = event.call
        from_number = call.from_.phone.number if isinstance(call.from_, Phone) else None
        to_number = call.to.phone.number if isinstance(call.to, Phone) else None
        logger.info(
            "call.incoming sessionId=%s from=%s to=%s",
            call.session_id,
            from_number,
            to_number,
        )
        return _handle_call_incoming(sinch_events_service, sinch_number, destination_number)

    # `commands` is required, so an empty list is how we return a 200 with no
    # SVAML actions, telling Sinch there's nothing to do for this event.
    return sinch_events_service.build_response(commands=[])


def _handle_call_incoming(
    sinch_events_service: SinchEvents,
    sinch_number: str,
    destination_number: str,
) -> VoiceSinchEventResponse:
    """Answer the call, greet the caller, then dial the agent and bridge both legs."""
    return sinch_events_service.build_incoming_call_response(
        commands=[
            {"command": "answer"},
            {
                "command": "messages",
                "messages_name": "greeting",
                "messages": [
                    {
                        "type": "SAY",
                        "say": {
                            "text": "Welcome to Acme. Please hold while we connect your call.",
                            "voice_name": "Emma",
                        },
                    }
                ],
            },
            {"command": "bridgeCall", "bridge_name": "inbound-bridge"},
            {
                "command": "dial",
                "call_name": "agent",
                "from_": {"type": "PHONE", "phone": {"number": sinch_number}},
                "to": {"type": "PHONE", "phone": {"number": destination_number}},
                "dial_timeout_duration_seconds": 30,
                "events": {
                    "on_answer": [{"command": "bridgeCall", "bridge_name": "inbound-bridge"}],
                    "on_hangup": [{"command": "hangup", "call_name": "incoming"}],
                    "on_timeout": [{"command": "hangup", "call_name": "incoming"}],
                },
            },
        ],
        call_name="incoming",
        events={"on_hangup": [{"command": "hangup", "call_name": "agent"}]},
    )
