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

# The SVAML commands to validate
commands = [
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
]

response = sinch_client.voice.v2.svaml.validate(commands=commands)

print(f"Successfully validated SVAML payload.\n{response}")
