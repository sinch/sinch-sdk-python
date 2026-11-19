import os
import uuid

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
recipients = [
    os.environ.get("DEST_1") or "MY_DEST_1",
    os.environ.get("DEST_2") or "MY_DEST_2",
]
max_cps = int(os.environ.get("MAX_CPS") or "5")
ttl_seconds = int(os.environ.get("TTL_SECONDS") or "1800")

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

# SVAML commands: dial @toNumber -> on answer TTS -> hangup
commands = CommandsSequenceCreator().dial(
    "@toNumber",
    from_=sinch_number,
    name="batch-reminder",
    timeout_duration_seconds=30,
    max_duration_seconds=120,
    on_answer=CommandsSequenceCreator().text(
        "Hello, this is an automated reminder from Sinch. Goodbye.",
        "Emma",
        on_finish=Calls.hangup(),
    ),
    on_hangup=Calls.hangup(),
)

# `parameters` is a list; each entry queues one call using that
# entry's placeholder values. One request, however many destinations.
parameters = [{"toNumber": recipient} for recipient in recipients]

print(
    f"Submitting batch to {', '.join(recipients)} "
    f"(maxCps={max_cps}, ttlSeconds={ttl_seconds}) ..."
)

response = sinch_client.voice.v2.batches.start(
    commands=commands,
    parameters=parameters,
    batch_options={"max_cps": max_cps, "ttl_seconds": ttl_seconds},
)

print(f"Batch created:\n{response}")
