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
)

# The ID of the service
service_id = "SERVICE_ID"

# The new name of the service
name = "Updated from Python SDK snippet"

response = sinch_client.voice.v2.services.update(service_id=service_id, name=name)

print(f"Successfully updated service.\n{response}")
