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

# The ID of the Conversation application the contact belongs to
conversation_application_id = "APPLICATION_ID"

# The ID of the contact to retrieve the channel profile for
conversation_contact_id = "CONTACT_ID"

# The channel associated with the contact
conversation_channel = "MESSENGER"

response = sinch_client.conversation.contacts.get_channel_profile(
    app_id=conversation_application_id,
    channel=conversation_channel,
    recipient={
        "contact_id": conversation_contact_id
    }
)

print(f"Successfully retrieved channel profile.\n{response}")
