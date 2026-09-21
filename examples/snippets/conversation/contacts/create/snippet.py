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
    conversation_region=os.environ.get("SINCH_CONVERSATION_REGION") or "MY_CONVERSATION_REGION"
)

# The channel to use for the contact
recipient_channel = "SMS"
# The phone number of the contact to create
recipient_phone_number = "RECIPIENT_PHONE_NUMBER"
# The display name of the contact to create
contact_display_name = "Created from Python SDK snippet"
# The language of the contact
language = "FR"
# The channel identities the contact is reachable on
channel_identities = [
    {"channel": recipient_channel, "identity": recipient_phone_number}
]

response = sinch_client.conversation.contacts.create(
    channel_identities=channel_identities,
    display_name=contact_display_name,
    language=language,
)

print(f"Successfully created contact.\n{response}")
