"""
Sinch Python Snippet

TODO: Update links when v2 is released.
This snippet is available at https://github.com/sinch/sinch-sdk-python/blob/v2.0/docs/snippets/
"""

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

# Example: Encode message body as Base64
message = "Hello, this is a binary message!"
body = base64.b64encode(message.encode('utf-8')).decode('utf-8')

# Example: UDH header (HEX encoded)
udh = "06050423F423F4"

response = sinch_client.sms.batches.send_binary(
    to=["+1234567890"],
    from_="+2345678901",
    body=body,
    udh=udh
)

print(f"Batch sent:\n{response}")
