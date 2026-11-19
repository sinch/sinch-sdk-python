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
caller_number = os.environ.get("CALLER_NUMBER") or "MY_CALLER_NUMBER"
primary_number = os.environ.get("PRIMARY_NUMBER") or "MY_PRIMARY_NUMBER"
fallback_number = os.environ.get("FALLBACK_NUMBER") or "MY_FALLBACK_NUMBER"

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

join_bridge = (
    CommandsSequenceCreator().stop_messages("hold").bridge_call("fwd-bridge")
)

# SVAML commands: dial the caller -> on answer play hold prompt, join the bridge
# and dial the primary -> on primary timeout dial the fallback -> on fallback
# timeout hang up the caller
commands = CommandsSequenceCreator().dial(
    caller_number,
    from_=sinch_number,
    name="caller",
    timeout_duration_seconds=30,
    on_answer=CommandsSequenceCreator()
    # Step 1: play a hold prompt while we try the primary
    .text("Connecting your call.", "Emma", name="hold")
    # Step 2: caller joins the bridge (created on first reference)
    .bridge_call("fwd-bridge")
    # Step 3: dial the primary number
    .dial(
        primary_number,
        from_=sinch_number,
        name="primary",
        timeout_duration_seconds=20,
        # Primary answered: stop the hold prompt, bridge them
        on_answer=join_bridge,
        # Primary didn't answer: try the fallback
        on_timeout=Calls.dial(
            fallback_number,
            from_=sinch_number,
            name="fallback",
            timeout_duration_seconds=20,
            on_answer=join_bridge,
            on_timeout=Calls.hangup("caller"),
        ),
    ),
    on_hangup=CommandsSequenceCreator().hangup("primary").hangup("fallback"),
)

response = sinch_client.voice.v2.calls.start(
    commands=commands
)

print(f"Call created successfully:\n{response}")
