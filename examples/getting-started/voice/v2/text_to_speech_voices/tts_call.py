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

# SVAML commands: dial -> on answer speak one line of TTS -> hangup
commands = CommandsSequenceCreator().dial(
    destination_number,
    from_=sinch_number,
    name="tts-hello",
    timeout_duration_seconds=30,
    max_duration_seconds=120,
    on_answer=CommandsSequenceCreator().text(
        "Hello. This is text to speech from the Sinch Voice API.",
        "Emma",
        name="hello",
        on_finish=Calls.hangup(),
    ),
    on_hangup=Calls.hangup(),
)

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Call created successfully:\n{response}")
