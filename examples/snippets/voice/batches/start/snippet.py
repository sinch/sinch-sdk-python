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

# The Sinch phone number to call from
from_phone_number = (
    os.environ.get("SINCH_PHONE_NUMBER") or "MY_SINCH_PHONE_NUMBER"
)

# The parameters for the batch calls, specifying the recipient phone numbers.
parameters = [
    {"to_number": "RECIPIENT_PHONE_NUMBER_1"},
    {"to_number": "RECIPIENT_PHONE_NUMBER_2"},
]

# The command dialing out to the recipients specified in the parameters
dial_command = {
    "command": "dial",
    "call_name": "Python_SDK_Snippet_Call",
    "from_": {"type": "PHONE", "phone": {"number": from_phone_number}},
    "to": {"type": "PHONE", "phone": {"number": "@to_number"}},
    "events": {
        "on_answer": [
            {
                "command": "messages",
                "messages": [
                    {
                        "type": "SAY",
                        "say": {
                            "text": "Hello, your call is now connected.",
                            "voice_name": "Emma",
                        },
                    }
                ],
            }
        ],
        "on_hangup": [{"command": "hangup"}],
    },
}

# The SVAML commands describing the call flow
commands = [dial_command]

response = sinch_client.voice.v2.batches.start(
    commands=commands, parameters=parameters
)

print(f"Batch successfully started.\n{response}")
