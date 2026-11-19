import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import (
    CommandsSequenceCreator,
    Recording,
)

load_dotenv()

project_id = os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID"
key_id = os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID"
key_secret = os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
sinch_number = os.environ.get("SINCH_NUMBER") or "MY_SINCH_NUMBER"
destination_number = (
    os.environ.get("DESTINATION_NUMBER") or "MY_DESTINATION_NUMBER"
)
storage_destination_url = (
    os.environ.get("STORAGE_DESTINATION_URL") or "MY_STORAGE_DESTINATION_URL"
)
storage_credentials = (
    os.environ.get("STORAGE_CREDENTIALS") or "MY_STORAGE_CREDENTIALS"
)

# Infer the storage provider from the destination URL scheme
if storage_destination_url.startswith("s3://"):
    storage_destination = "AWS"
elif storage_destination_url.startswith("gs://"):
    storage_destination = "GCP"
else:
    storage_destination = "AZURE"

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

# SVAML commands: dial -> on answer start recording and play a recording notice
# -> on hangup stop recording, which uploads the file to the storage bucket
commands = CommandsSequenceCreator().dial(
    destination_number,
    from_=sinch_number,
    name="recorded-call",
    timeout_duration_seconds=30,
    max_duration_seconds=3600,
    on_answer=CommandsSequenceCreator()
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
        "This call is being recorded.",
        "Emma",
        name="recording-notice",
    ),
    on_hangup=CommandsSequenceCreator().stop_recording("main-recording"),
)

print(
    f"Calling {destination_number} with recording enabled "
    f"({storage_destination}) ..."
)

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Call created with recording:\n{response}")
print(f"Recording will be uploaded to: {storage_destination_url}")
