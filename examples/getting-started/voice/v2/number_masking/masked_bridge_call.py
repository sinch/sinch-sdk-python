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
# Default the two legs; override with two real phones for a proper test
party_a_number = os.environ.get("PARTY_A_NUMBER") or destination_number
party_b_number = os.environ.get("PARTY_B_NUMBER") or sinch_number

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

# SVAML commands: dial Party A -> on answer greet, join the bridge and dial
# Party B -> on Party B answer join the bridge. Both legs show the Sinch number.
commands = CommandsSequenceCreator().dial(
    party_a_number,
    from_=sinch_number,
    name="party-a",
    timeout_duration_seconds=30,
    on_answer=CommandsSequenceCreator()
    .text(
        "Please hold while we connect the other party.",
        "Emma",
        name="greeting",
    )
    .bridge_call("masked-bridge")
    .dial(
        party_b_number,
        from_=sinch_number,
        name="party-b",
        timeout_duration_seconds=30,
        on_answer=Calls.bridge_call("masked-bridge"),
        on_hangup=Calls.hangup("party-a"),
    ),
    on_hangup=Calls.hangup("party-b"),
)

print(
    f"Initiating masked bridge call between {party_a_number} "
    f"and {party_b_number} ..."
)
print(f"(Both parties will see {sinch_number} as the caller ID)")

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Bridge call created successfully:\n{response}")
