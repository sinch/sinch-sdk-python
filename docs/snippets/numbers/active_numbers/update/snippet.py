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

phone_number_to_update = os.environ.get("SINCH_PHONE_NUMBER") or "MY_SINCH_PHONE_NUMBER"
updated_display_name = "Updated DISPLAY_NAME"

response = sinch_client.numbers.update(
    phone_number=phone_number_to_update,
    display_name=updated_display_name
)

print("Updated Number:\n", response)
