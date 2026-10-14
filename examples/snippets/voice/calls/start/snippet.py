"""
Sinch Python Snippet

This snippet is available at https://github.com/sinch/sinch-sdk-python/tree/main/examples/snippets
"""

import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import (
    Calls,
    CommandsSequenceCreator,
)

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
)

# The phone number to be used as the caller ID, in E.164 format (e.g., +12025550123)
sinch_phone_number = (
    os.environ.get("SINCH_PHONE_NUMBER") or "MY_SINCH_PHONE_NUMBER"
)

# The phone number you want to call, in E.164 format (e.g., +12025550123)
recipient_phone_number = "RECIPIENT_PHONE_NUMBER"

# The SVAML commands describing the call flow: dial out to the recipient
commands = CommandsSequenceCreator().dial(
    recipient_phone_number,
    from_=sinch_phone_number,
    name="Python_SDK_Snippet_Call",
    on_answer=CommandsSequenceCreator().text(
        "Hello, your call is now connected.",
        "Emma",
        on_finish=Calls.hangup(),
    ),
)

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Call Successfully started.\n{response}")
