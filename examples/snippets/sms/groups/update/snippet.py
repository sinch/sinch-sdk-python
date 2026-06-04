"""
Sinch Python Snippet

This snippet is available at https://github.com/sinch/sinch-sdk-python/tree/main/examples/snippets
"""

import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.sms.api.v1.groups_apis import GroupResponse

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
    sms_region=os.environ.get("SINCH_SMS_REGION") or "MY_SMS_REGION"
)

# The ID of the group to update
group_id = "GROUP_ID"

response: GroupResponse = sinch_client.sms.groups.update(
    group_id=group_id,
    add=["+1234567890"],
    remove=["+1987654321"],
    name="Renamed Group",
)

print(f"Group updated:\n{response}")
