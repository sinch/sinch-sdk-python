import os
from dotenv import load_dotenv
from sinch import SinchClient

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
    sms_region=os.environ.get("SINCH_SMS_REGION") or "MY_SMS_REGION"
)

# The ID of the batch to get delivery reports for
batch_id = "BATCH_ID"
# The phone number to get delivery reports for
recipient = "+1234567890"

response = sinch_client.sms.delivery_reports.get_for_number(
    batch_id=batch_id,
    recipient=recipient
)

print(f"Delivery report for recipient:\n{response}")
