import os
from dotenv import load_dotenv
from sinch import SinchClient
from sinch.domains.sms.models.v1.shared import MediaBody

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
    sms_region=os.environ.get("SINCH_SMS_REGION") or "MY_SMS_REGION"
)

batch_id = "MY_BATCH_ID"

body = MediaBody(
    url="https://example.com/image.jpg",
    message="Updated MMS message content"
)

response = sinch_client.sms.batches.replace_mms(
    batch_id=batch_id,
    to=["+1234567890"],
    from_="+2345678901",
    body=body
)

print(f"Replaced batch:\n{response}")
