import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import (
    Calls,
    CommandsSequenceCreator,
    Recording,
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
storage_destination_url = (
    os.environ.get("STORAGE_DESTINATION_URL") or "MY_STORAGE_DESTINATION_URL"
)
storage_credentials = (
    os.environ.get("STORAGE_CREDENTIALS") or "MY_STORAGE_CREDENTIALS"
)
port = int(os.environ.get("PORT") or "8081")

# Infer the storage provider from the destination URL scheme
if storage_destination_url.startswith("gs://"):
    storage_destination = "GCP"
elif storage_destination_url.startswith("s3://"):
    storage_destination = "AWS"
else:
    storage_destination = "AZURE"

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
        # SVAML commands: answer -> start recording -> play a recording notice
        response = sinch_events.build_incoming_call_response(
            commands=CommandsSequenceCreator()
            .answer()
            .recording(
                Recording.options(
                    storage_destination,
                    storage_destination_url,
                    storage_credentials,
                    format="MP3",
                    recording_type="COMBINED",
                    transcription_options={"is_enabled": True, "locale": "en-US"},
                ),
                name="main-recording",
            )
            .text(
                "This call may be recorded for quality and compliance purposes.",
                "Emma",
                name="recording-notice",
            ),
            # Add further SVAML commands here, e.g.:
            # .bridge_call("agent-bridge")
            on_hangup=Calls.hangup(),
        )
    else:
        print(f"Unhandled event: {event.event}")
        response = sinch_events.build_response(commands=[])

    return jsonify(sinch_events.serialize_response(response))


if __name__ == "__main__":
    print(f"Recording webhook server listening on port {port}")
    print(f"Storage: {storage_destination} -> {storage_destination_url}")
    print(f"(Use ngrok: ngrok http {port})")
    app.run(host="0.0.0.0", port=port)
