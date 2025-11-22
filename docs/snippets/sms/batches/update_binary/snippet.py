import os
import base64
from dotenv import load_dotenv
from sinch import SinchClient

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
    sms_region=os.environ.get("SINCH_SMS_REGION") or "MY_SMS_REGION"
)

# The ID of the batch to update
batch_id = "BATCH_ID"

# Example: UDH header (HEX encoded)
udh = "06050423F423F4"

# Example: Encode message body as Base64 (optional)
message = "Updated binary message body"
body = base64.b64encode(message.encode('utf-8')).decode('utf-8')

response = sinch_client.sms.batches.update_binary(
    batch_id=batch_id,
    udh=udh,
    body=body,
    to_add=["+1987654321"]
)

print(f"Updated batch:\n{response}")
