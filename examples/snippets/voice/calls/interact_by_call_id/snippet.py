"""
Sinch Python Snippet

This snippet is available at https://github.com/sinch/sinch-sdk-python/tree/main/examples/snippets
"""

import os

from dotenv import load_dotenv

from sinch import SinchClient

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
)

# The ID of the ongoing call to interact with
call_id = "CALL_ID"

# The SVAML commands to interact with the ongoing call
commands = [{"command": "hangup"}]

sinch_client.voice.v2.calls.interact_by_call_id(
    call_id=call_id, commands=commands
)

print("Successfully submitted commands to the call.")
