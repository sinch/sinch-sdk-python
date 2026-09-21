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

# The ID of the contact to merge into (the destination contact)
destination_id = "DESTINATION_CONTACT_ID"

# The ID of the contact to merge from (the source contact)
source_id = "SOURCE_CONTACT_ID"

response = sinch_client.conversation.contacts.merge_contact(
    destination_id=destination_id,
    source_id=source_id
)

print(f"Successfully merged contacts.\n{response}")
