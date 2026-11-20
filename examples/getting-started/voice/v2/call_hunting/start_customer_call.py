import os

from dotenv import load_dotenv

from sinch import SinchClient
from sinch.domains.voice.helpers.v2.svaml import CommandsSequenceCreator

load_dotenv()

project_id = os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID"
key_id = os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID"
key_secret = os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
sinch_number = os.environ.get("SINCH_NUMBER") or "MY_SINCH_NUMBER"
customer_number = os.environ.get("CUSTOMER_NUMBER") or "MY_CUSTOMER_NUMBER"

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

commands = CommandsSequenceCreator().dial(
    customer_number,
    from_=sinch_number,
    name="customer",
    timeout_duration_seconds=30,
)

response = sinch_client.voice.v2.calls.start(commands=commands)

print(f"Call created successfully:\n{response}")
