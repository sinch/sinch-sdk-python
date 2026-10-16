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

# The ID of the Conversation App to send the event from
app_id = "CONVERSATION_APP_ID"
# The phone number to send the Event to, in E.164 format
recipient_phone_number = "RECIPIENT_PHONE_NUMBER"

response = sinch_client.conversation.events.send(
    app_id=app_id,
    event={
        "composing_event": {}
    },
    recipient_identities=[
        {
            "channel": "RCS",
            "identity": recipient_phone_number
        }
    ]
)

print(f"Successfully sent event.\n{response}")
