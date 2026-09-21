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

# The phone number of the recipient to call
to_phone_number = "RECIPIENT_PHONE_NUMBER"

# The command dialing out to the recipient
dial_command = {
    "command": "dial",
    "call_name": "Python_SDK_Snippet_Call",
    "from_": {"type": "PHONE", "phone": {"number": from_phone_number}},
    "to": {"type": "PHONE", "phone": {"number": to_phone_number}},
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

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Call Successfully started.\n{response}")
