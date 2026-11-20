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
agent_numbers = os.environ.get("AGENT_NUMBERS") or "MY_AGENT_NUMBER"
port = int(os.environ.get("PORT") or "3000")

agents = [n.strip() for n in agent_numbers.split(",") if n.strip()]

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)
sinch_events = sinch_client.voice.v2.sinch_events

# In-memory hunt cursor: session ID -> index of the agent being dialed.
cursors = {}

FAILED_EVENTS = ("call.timeout", "call.busy", "call.rejected", "call.failed")

app = Flask(__name__)


def dial_agent(index):
    return Calls.dial(
        agents[index],
        from_=sinch_number,
        name=f"agent-{index}",
        timeout_duration_seconds=20,
    )


@app.post("/voice/events")
def voice_events():
    event: VoiceSinchEventRequest = sinch_events.parse_event(
        request.get_data(), dict(request.headers)
    )
    session_id = event.call.session_id
    call_name = event.call.call_name or ""

    print(f"event={event.event} sessionId={session_id} callName={call_name}")

    response: VoiceSinchEventResponse
    if event.event == "call.incoming":
        # Inbound call: the inbound leg is the customer. Answer, join the
        # bridge and dial the first agent
        cursors[session_id] = 0
        response = sinch_events.build_incoming_call_response(
            commands=CommandsSequenceCreator()
            .answer()
            .text(
                "Please hold while we find an agent.",
                "Emma_3",
                name="hold",
            )
            .bridge_call("hunt-bridge")
            .command(dial_agent(0)),
            on_hangup=Calls.hangup(),
        )
    elif event.event == "call.answered" and call_name == "customer":
        # Outbound customer leg answered: play the hold message, join the
        # bridge and dial the first agent
        cursors[session_id] = 0
        response = sinch_events.build_response(
            commands=CommandsSequenceCreator()
            .text(
                "Please hold while we find an agent.",
                "Emma_3",
                name="hold",
            )
            .bridge_call("hunt-bridge")
            .command(dial_agent(0))
        )
    elif event.event == "call.answered" and call_name.startswith("agent-"):
        # Agent answered: stop the hold message and bridge them in
        response = sinch_events.build_response(
            commands=CommandsSequenceCreator()
            .stop_messages("hold")
            .bridge_call("hunt-bridge")
        )
    elif event.event in FAILED_EVENTS and call_name.startswith("agent-"):
        # Agent didn't connect: advance the cursor and try the next agent
        index = cursors.get(session_id, 0) + 1
        cursors[session_id] = index
        if index >= len(agents):
            # No more agents: apologise and hang up
            cursors.pop(session_id, None)
            response = sinch_events.build_response(
                commands=CommandsSequenceCreator().text(
                    "We are sorry, no agent is available. "
                    "Please try again later.",
                    "Emma_3",
                    name="noanswer",
                    on_finish=Calls.hangup(),
                )
            )
        else:
            response = sinch_events.build_response(commands=dial_agent(index))
    else:
        if event.event == "call.hangup":
            cursors.pop(session_id, None)
        response = sinch_events.build_response(commands=[])

    return jsonify(sinch_events.serialize_response(response))


if __name__ == "__main__":
    print(f"Hunt webhook server listening on :{port}")
    print(
        "Configure service callBehavior.webhook.url -> "
        "https://<your-ngrok>/voice/events"
    )
    app.run(host="0.0.0.0", port=port)
