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

# The ID of the conversation event destination to retrieve
event_destination_id = "EVENT_DESTINATION_ID"

response = sinch_client.conversation.event_destinations.get(
    event_destination_id=event_destination_id
)

print(f"Event destination details:\n{response}")
