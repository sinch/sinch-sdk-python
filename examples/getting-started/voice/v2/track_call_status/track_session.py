import os
import sys
import time

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import (
    Calls,
    CommandsSequenceCreator,
)
from sinch.domains.voice.models.v2.sessions.response.session_response import (
    SessionResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call

load_dotenv()

project_id = os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID"
key_id = os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID"
key_secret = os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
sinch_number = os.environ.get("SINCH_NUMBER") or "MY_SINCH_NUMBER"
destination_number = (
    os.environ.get("DESTINATION_NUMBER") or "MY_DESTINATION_NUMBER"
)

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

commands = CommandsSequenceCreator().dial(
    destination_number,
    from_=sinch_number,
    name="tracked",
    timeout_duration_seconds=30,
    on_answer=CommandsSequenceCreator().text(
        "This call is being tracked. Goodbye.",
        "Emma",
        on_finish=Calls.hangup(),
    ),
    on_hangup=Calls.hangup(),
)

# 1. Start the call. Inline events play a short message and hang up.
start = sinch_client.voice.v2.calls.start(
    commands=commands,
)
session_id = start.session_id
print(f"Started sessionId={session_id}")

# 2. Poll until COMPLETED (the only final session state), bounded with backoff.
delay, max_delay, attempt, max_attempts = 2, 15, 0, 40
completed = False
while attempt < max_attempts:
    state = sinch_client.voice.v2.sessions.get(session_id=session_id).state
    print(f"state={state}")
    if state == "COMPLETED":  # terminal state -> stop
        completed = True
        break
    attempt += 1
    time.sleep(delay)
    delay = min(delay * 2, max_delay)

if not completed:
    sys.exit(
        f"Session {session_id} did not reach COMPLETED "
        f"after {max_attempts} attempts"
    )

# 3. Print per-leg results (callName is NOT returned by the API).
session: SessionResponse = sinch_client.voice.v2.sessions.get(
    session_id=session_id
)
call: Call
for call in session.calls:
    print(
        f"call_id={call.call_id} "
        f"call_result={call.call_result} "
        f"call_reason={call.call_reason} "
        f"call_duration_seconds={call.call_duration_seconds} "
        f"answer_time={call.answer_time}"
    )
