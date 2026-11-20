import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.services import CallBehavior

load_dotenv()

project_id = os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID"
key_id = os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID"
key_secret = os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
service_id = os.environ.get("SINCH_SERVICE_ID") or "MY_SERVICE_ID"
callback_url = os.environ.get("CALLBACK_URL") or "MY_CALLBACK_URL"

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

# Send the service's call events to the hunt server, with the same URL as fallback
response = sinch_client.voice.v2.services.update(
    service_id=service_id,
    call_behavior=CallBehavior.event_destination(
        f"{callback_url}/voice/events",
        fallback_url=f"{callback_url}/voice/events",
    ),
)

print(f"Service updated:\n{response}")
