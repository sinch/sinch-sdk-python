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

# The ID of the Conversation App that must contain the target channels for transcoding
app_id = "CONVERSATION_APP_ID"
# The channels for which the message is transcoded. Add other channels as needed, e.g. "SMS", "RCS", "MESSENGER"
channels = ["WHATSAPP"]
# The message to transcode, in the Conversation API format
app_message = {
    "location_message": {
        "title": "Coordinates title",
        "coordinates": {
            "latitude": 59.3360453,
            "longitude": 18.0117363
        }
    }
}

response = sinch_client.conversation.transcoding.transcode_message(
    app_id=app_id,
    app_message=app_message,
    channels=channels
)

print(f"Successfully transcoded the message.\n{response}")
