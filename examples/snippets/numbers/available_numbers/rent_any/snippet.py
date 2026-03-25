"""
Sinch Python Snippet

This snippet is available at https://github.com/sinch/sinch-sdk-python/tree/main/examples/snippets
"""

import os
from dotenv import load_dotenv
from sinch import SinchClient
from sinch.domains.numbers.models.v1.types import SmsConfigurationDict

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
)

# The service plan ID to associate with the phone number
service_plan_id = os.environ.get("SINCH_SERVICE_PLAN_ID") or "MY_SERVICE_PLAN_ID"
sms_configuration: SmsConfigurationDict = {
    "service_plan_id": service_plan_id,
}
# The URL to receive the notifications about provisioning events
event_destination_target = "CALLBACK_URL"

response = sinch_client.numbers.rent_any(
    region_code="US",
    number_type="LOCAL",
    capabilities=["SMS", "VOICE"],
    sms_configuration=sms_configuration,
    event_destination_target=event_destination_target
)

print("Rented Number:\n", response)
