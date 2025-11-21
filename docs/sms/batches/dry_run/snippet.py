import os
from dotenv import load_dotenv
from sinch import SinchClient
from sinch.domains.sms.models.v1.internal.dry_run_request import DryRunTextRequest

load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID",
    key_id=os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID",
    key_secret=os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET",
    sms_region=os.environ.get("SINCH_SMS_REGION") or "MY_SMS_REGION"
)

request = DryRunTextRequest(
    to=["+1234567890"],
    from_="+2345678901",
    body="Test message for dry run"
)

response = sinch_client.sms.batches.dry_run(request=request)

print(f"Dry run result:\n{response}")
