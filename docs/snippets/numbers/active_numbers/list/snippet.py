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

active_numbers = sinch_client.numbers.list(
    region_code="US",
    number_type="LOCAL"
)

page_counter = 1
while True:
    print(f"Page {page_counter} List of Numbers: {active_numbers}")

    if not active_numbers.has_next_page:
        break

    active_numbers = active_numbers.next_page()
    page_counter += 1
