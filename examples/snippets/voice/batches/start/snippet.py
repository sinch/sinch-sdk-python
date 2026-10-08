"""
Sinch Python Snippet

This snippet is available at https://github.com/sinch/sinch-sdk-python/tree/main/examples/snippets
"""

import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import Calls, Messages

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

# The parameters for the batch calls, specifying the recipient phone numbers.
parameters = [
    {"to_number": "RECIPIENT_PHONE_NUMBER_1"},
    {"to_number": "RECIPIENT_PHONE_NUMBER_2"},
]

# The command dialing out to the recipients specified in the parameters
dial = Calls.dial(
    "@to_number",
    from_=sinch_phone_number,
    name="Python_SDK_Snippet_Call",
    on_answer=[
        Messages.start(
            [Messages.text("Hello, your call is now connected.", "Emma")],
            on_finish=[Calls.hangup()],
        )
    ],
)

# The SVAML commands describing the call flow
commands = [dial]

response = sinch_client.voice.v2.batches.start(
    commands=commands, parameters=parameters
)

print(f"Batch successfully started.\n{response}")
