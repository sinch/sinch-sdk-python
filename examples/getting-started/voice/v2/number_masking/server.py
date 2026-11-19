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


@app.post("/webhook")
def webhook():
    event: VoiceSinchEventRequest = sinch_events.parse_event(
        request.get_data(), dict(request.headers)
    )

    print(f"Received webhook event: {event.event}")
    print(event.call)

    response: VoiceSinchEventResponse
    if event.event == "call.incoming":
        # "call_name" names the inbound (caller) leg and "on_hangup" handles
        # the caller hanging up
        response = sinch_events.build_incoming_call_response(
            commands=CommandsSequenceCreator()
            .answer()
            .text(
                "Please hold while we connect your call.",
                "Emma",
                name="greeting",
            )
            # Add Party A to a named bridge
            .bridge_call("main-bridge")
            .dial(
                # In production, look up the destination from your DB (event.call.to)
                destination_number,
                # Party B sees the Sinch number
                from_=sinch_number,
                name="callee",
                timeout_duration_seconds=30,
                on_answer=Calls.bridge_call("main-bridge"),
                on_hangup=Calls.hangup("caller"),
            ),
            call_name="caller",
            on_hangup=Calls.hangup("callee"),
        )
    else:
        print(f"Unhandled event: {event.event}")
        response = sinch_events.build_response(commands=[])

    return jsonify(sinch_events.serialize_response(response))


if __name__ == "__main__":
    print(f"Number masking webhook server listening on port {port}")
    app.run(host="0.0.0.0", port=port)
