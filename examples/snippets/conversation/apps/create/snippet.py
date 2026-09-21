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

# The display name for the app
display_name = "[Python SDK: Conversation App] Sample app"

# The service plan ID for the SMS channel
sms_service_plan_id = os.environ.get("SINCH_SERVICE_PLAN_ID") or "SMS_SERVICE_PLAN_ID"

# The API token for the SMS channel
sms_api_token = "SMS_API_TOKEN"

# The channel credentials for the app
channel_credentials = {
    "SMS": {
        "claimed_identity": sms_service_plan_id,
        "token": sms_api_token
    }
}

response = sinch_client.conversation.apps.create(
    display_name=display_name,
    channel_credentials=channel_credentials,
)

print(f"Successfully created app.\n{response}")


