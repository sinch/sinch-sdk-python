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


@app.post("/webhook")
def webhook():
    event: VoiceSinchEventRequest = sinch_events.parse_event(
        request.get_data(), dict(request.headers)
    )

    print(f"Received event: {event.event}, callId: {event.call.call_id}")

    response: VoiceSinchEventResponse
    if event.event == "call.incoming":
        # Inbound call: answer and run AMD as the first command after answering.
        # AMD fires one of: onHuman, onMachine, onBeep, onUnknown.
        response = sinch_events.build_response(
            commands=CommandsSequenceCreator()
            .answer()
            .amd(
                # Live human: play a personalized greeting
                on_human=CommandsSequenceCreator().text(
                    "Hello! This is a call from Acme Corp. "
                    "An agent will be with you shortly.",
                    "Emma",
                    name="human-greeting",
                    on_finish=Calls.hangup(),
                ),
                # Machine greeting (no beep yet): hang up silently
                on_machine=Calls.hangup(),
                # Beep detected: leave voicemail right after the beep
                on_beep=CommandsSequenceCreator().text(
                    "Hi, this is Acme Corp calling about your recent inquiry. "
                    "Please call us back at 555-1234. Thank you.",
                    "Emma",
                    name="voicemail-message",
                    on_finish=Calls.hangup(),
                ),
                # Unknown result: hang up safely
                on_unknown=Calls.hangup(),
            )
        )
    elif event.event.startswith("call.amd."):
        # AMD verdict events: this is how you see which branch fired, server-side
        print(f"AMD verdict: {event.event}")
        response = sinch_events.build_response(commands=[])
    else:
        print(f"Unhandled event: {event.event}")
        response = sinch_events.build_response(commands=[])

    return jsonify(sinch_events.serialize_response(response))


if __name__ == "__main__":
    print(f"AMD callback server listening on port {port}")
    print(
        "Set your Sinch service webhook URL to: "
        f"http://localhost:{port}/webhook"
    )
    print(f"(Use ngrok: ngrok http {port})")
    app.run(host="0.0.0.0", port=port)
