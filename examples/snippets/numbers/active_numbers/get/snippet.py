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
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
)

# The active phone number to retrieve details for in E.164 format
phone_number = os.environ.get("SINCH_PHONE_NUMBER") or "MY_PHONE_NUMBER"

response = sinch_client.numbers.get(phone_number=phone_number)

print(f"Rented number details:\n{response}")
