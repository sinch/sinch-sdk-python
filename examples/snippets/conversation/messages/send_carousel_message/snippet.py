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

# The ID of the Conversation App to send the message from
app_id = "CONVERSATION_APP_ID"
# The phone number of the recipient in E.164 format (e.g. +46701234567)
recipient_identities = [
    {
        "channel": "RCS",
        "identity": "RECIPIENT_PHONE_NUMBER"
    }
]

carousel_message = {
    "cards": [
        {
            "title": "Card 1",
            "description": "First card description",
            "choices": [{"text_message": {"text": "Option 1"}}],
        },
        {
            "title": "Card 2",
            "description": "Second card description",
            "choices": [{"url_message": {"title": "Link", "url": "https://example.com"}}],
        },
    ],
}

response = sinch_client.conversation.messages.send_carousel_message(
    app_id=app_id,
    carousel_message=carousel_message,
    recipient_identities=recipient_identities
)

print(f"Successfully sent carousel message.\n{response}")
