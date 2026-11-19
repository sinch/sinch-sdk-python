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
    ce = {
        "type": request.headers.get("ce-type"),
        "source": request.headers.get("ce-source"),
        "id": request.headers.get("ce-id"),
        "time": request.headers.get("ce-time"),
        "specversion": request.headers.get("ce-specversion"),
    }
    event: VoiceSinchEventRequest = sinch_events.parse_event(
        request.get_data(), dict(request.headers)
    )

    print(f"ce={ce}")
    print(f"event={event.event}")
    print(f"call={event.call}")

    response: VoiceSinchEventResponse
    if event.event == "call.incoming":
        # Return the call flow directly; on_hangup is honored here
        response = sinch_events.build_incoming_call_response(
            commands=CommandsSequenceCreator()
            .answer()
            .text(
                "Thank you for calling. Goodbye.",
                "Emma",
                on_finish=Calls.hangup(),
            ),
            on_hangup=Calls.hangup(),
        )
    else:
        response = sinch_events.build_response(commands=[])

    return jsonify(sinch_events.serialize_response(response))


if __name__ == "__main__":
    print(f"Webhook receiver on :{port}")
    print(
        "Point callBehavior.webhook.url -> https://<your-ngrok>/voice/events"
    )
    app.run(host="0.0.0.0", port=port)
