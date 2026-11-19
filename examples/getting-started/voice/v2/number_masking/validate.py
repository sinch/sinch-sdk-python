import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import (
    Calls,
    CommandsSequenceCreator,
)

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

# SVAML commands to validate: the masking flow server.py returns on call.incoming
commands = (
    CommandsSequenceCreator()
    .answer()
    .text("Please hold while we connect your call.", "Emma", name="greeting")
    .bridge_call("main-bridge")
    .dial(
        destination_number,
        from_=sinch_number,
        name="callee",
        timeout_duration_seconds=30,
        on_answer=Calls.bridge_call("main-bridge"),
        on_hangup=Calls.hangup("caller"),
    )
)

response = sinch_client.voice.v2.svaml.validate(
    commands=commands,
    call_name="caller",
    on_hangup=Calls.hangup("callee"),
    validation_type="STRICT",
)

print(response)
