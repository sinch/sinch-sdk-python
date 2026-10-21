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

# The id of the template to be updated
template_id = "TEMPLATE_ID"

response = sinch_client.conversation.templates.update(
    template_id=template_id,
    description="Updated description from Python SDK",
    version=2,
    default_translation="en-US",
    translations=[
        {
            "version": "1",
            "language_code": "en-US",
            "text_message": {"text": "Updated text from Python SDK"},
        }
    ],
)

print(f"Successfully updated template.\n{response}")
