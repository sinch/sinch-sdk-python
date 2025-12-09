"""
Sinch Python Snippet

TODO: Update links when v2 is released.
This snippet is available at https://github.com/sinch/sinch-sdk-python/blob/v2.0/docs/snippets/
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

phone_number = os.environ.get("SINCH_PHONE_NUMBER") or "MY_SINCH_PHONE_NUMBER"
released_number = sinch_client.numbers.release(
    phone_number=phone_number
)

print("Released Number:", released_number)
