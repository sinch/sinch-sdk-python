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
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
    conversation_region=os.environ.get("SINCH_CONVERSATION_REGION") or "MY_CONVERSATION_REGION"
)

# Channel identities to fetch the last message
channel_identities = ["CHANNEL_IDENTITY_1", "CHANNEL_IDENTITY_2"]

messages = sinch_client.conversation.messages.list_last_messages_by_channel_identity(
    channel_identities=channel_identities,
)

page_counter = 1
while True:
    print(f"Page {page_counter} Last messages: {messages}")

    if not messages.has_next_page:
        break

    messages = messages.next_page()
    page_counter += 1
