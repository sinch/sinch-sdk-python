import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import (
    Calls,
    CommandsSequenceCreator,
)
from sinch.domains.voice.models.v2.sinch_events.voice_sinch_event_request import (
    VoiceSinchEventRequest,
)
from sinch.domains.voice.models.v2.sinch_events.voice_sinch_event_response import (
    VoiceSinchEventResponse,
)

load_dotenv()

project_id = os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID"
key_id = os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID"
key_secret = os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
sinch_number = os.environ.get("SINCH_NUMBER") or "MY_SINCH_NUMBER"
destination_number = (
    os.environ.get("DESTINATION_NUMBER") or "MY_DESTINATION_NUMBER"
)
port = int(os.environ.get("PORT") or "3000")

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)
sinch_events = sinch_client.voice.v2.sinch_events

app = Flask(__name__)


@app.post("/voice/events")
def voice_events():
    event: VoiceSinchEventRequest = sinch_events.parse_event(
        request.get_data(), dict(request.headers)
    )

    print(f"event={event.event} sessionId={event.call.session_id}")

    response: VoiceSinchEventResponse
    if event.event == "call.incoming":
        # SVAML commands: answer -> greet -> bridge with the agent leg dialed below
        response = sinch_events.build_incoming_call_response(
            commands=CommandsSequenceCreator()
            .answer()
            .text(
                "Welcome to Acme. Please hold while we connect your call.",
                "Emma",
                name="greeting",
            )
            .bridge_call("inbound-bridge")
            .dial(
                destination_number,
                from_=sinch_number,
                name="agent",
                timeout_duration_seconds=30,
                on_answer=Calls.bridge_call("inbound-bridge"),
                on_hangup=Calls.hangup("incoming"),
                on_timeout=Calls.hangup("incoming"),
            ),
            call_name="incoming",
            on_hangup=Calls.hangup("agent"),
        )
    else:
        # For all other events, acknowledge with no commands
        response = sinch_events.build_response(commands=[])

    return jsonify(sinch_events.serialize_response(response))


if __name__ == "__main__":
    print(f"Inbound PSTN webhook server on :{port}")
    app.run(host="0.0.0.0", port=port)
