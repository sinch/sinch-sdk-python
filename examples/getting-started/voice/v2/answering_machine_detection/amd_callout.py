import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import (
    Amd,
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

# The `amd` command must be placed in the `onAnswer` event of a `dial` command.
# It fires different SVAML commands based on what AMD detects.
commands = CommandsSequenceCreator().dial(
    destination_number,
    from_=sinch_number,
    name="amd-call",
    timeout_duration_seconds=45,
    max_duration_seconds=300,
    on_answer=Amd.activate(
        # Human picked up: play a personalized greeting
        on_human=CommandsSequenceCreator().text(
            "Hello! This is a call from Acme Corp. "
            "An agent will be with you shortly.",
            "Emma",
            name="human-greeting",
            on_finish=Calls.hangup(),
        ),
        # Machine greeting detected (beep not yet heard): just hang up
        on_machine=Calls.hangup(),
        # Beep detected: leave a voicemail message right now
        on_beep=CommandsSequenceCreator().text(
            "Hi, this is Acme Corp calling about your recent inquiry. "
            "Please call us back at 555-1234. Thank you.",
            "Emma",
            name="voicemail-message",
            on_finish=Calls.hangup(),
        ),
        # Unknown: hang up safely
        on_unknown=Calls.hangup(),
    ),
)

print(f"Placing AMD callout from {sinch_number} to {destination_number} ...")

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"AMD call created successfully:\n{response}")
