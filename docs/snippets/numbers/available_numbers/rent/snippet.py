"""
Sinch Python Snippet

TODO: Update links when v2 is released.
This snippet is available at https://github.com/sinch/sinch-sdk-python/blob/v2.0/docs/snippets/
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

phone_number_to_be_rented = "AVAILABLE_PHONE_NUMBER_TO_BE_RENTED"
service_plan_id_to_associate_with_the_number = os.environ.get("SINCH_SERVICE_PLAN_ID") or "MY_SERVICE_PLAN_ID"
sms_configuration: SmsConfigurationDict = {
    "service_plan_id": service_plan_id_to_associate_with_the_number
}

rented_number = sinch_client.numbers.rent(
    phone_number=phone_number_to_be_rented,
    sms_configuration=sms_configuration
)
print("Rented Number:\n", rented_number)
