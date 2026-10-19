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

# The ID of the Conversation to inject an event to
conversation_id = "CONVERSATION_ID"

# The phone number of the recipient to inject an event to
recipient_phone_number = "RECIPIENT_PHONE_NUMBER"

response = sinch_client.conversation.conversations.inject_event(
    conversation_id=conversation_id,
    app_event={
        "generic_event": {
            "payload": {
                "a_property_key": "a property value"
            }
        }
    },
    accept_time=datetime.now(timezone.utc),
    channel_identity={
        "channel": "RCS",
        "identity": recipient_phone_number
    },
    processing_mode="CONVERSATION"
)

print(f"Successfully injected the event.\n{response}")
