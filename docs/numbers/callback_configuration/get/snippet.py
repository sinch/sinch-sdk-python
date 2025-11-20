"""
Sinch Python Snippet

This snippet is available at https://github.com/sinch/sinch-sdk-python-snippets
"""

import os
from dotenv import load_dotenv
from sinch import SinchClient

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
)

response = sinch_client.numbers.callback_configuration.get()

print("Callback Configuration:\n", response)
