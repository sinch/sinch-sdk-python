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

# The ID of the session the call leg belongs to
session_id = "SESSION_ID"

# The name of the call leg within the session
call_name = "CALL_NAME"

# The SVAML commands to interact with the ongoing call
commands = [{"command": "hangup"}]

sinch_client.voice.v2.calls.interact_by_call_name(
    session_id=session_id, call_name=call_name, commands=commands
)

print("Successfully submitted commands to the call.")
