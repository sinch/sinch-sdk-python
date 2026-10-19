"""
Sinch Python Snippet

This snippet is available at https://github.com/sinch/sinch-sdk-python/tree/main/examples/snippets
"""

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from sinch import SinchClient

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
    conversation_region=os.environ.get("SINCH_CONVERSATION_REGION") or "MY_CONVERSATION_REGION"
)

# The ID of the Conversation to inject a message into
conversation_id = "CONVERSATION_ID"
# The ID of the Contact to inject a message into
contact_id = "CONTACT_ID"
# The phone number of the recipient in E.164 format as identity for a given channel
recipient_phone_number = "RECIPIENT_PHONE_NUMBER"

sinch_client.conversation.conversations.inject_message(
    conversation_id=conversation_id,
    contact_id=contact_id,
    channel_identity={
        "channel": "RCS",
        "identity": recipient_phone_number
    },
    direction="TO_CONTACT",
    accept_time=datetime.now(timezone.utc),
    contact_message={
        "text_message": {
            "text": "Text from Inject AppMessage"
        }
    }
)

print(f"Successfully injected the message into the conversation with ID {conversation_id}.")
