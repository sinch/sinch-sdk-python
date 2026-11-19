import os
import sys
import time

from dotenv import load_dotenv

from sinch import SinchClient

load_dotenv()

project_id = os.environ.get("SINCH_PROJECT_ID") or "MY_PROJECT_ID"
key_id = os.environ.get("SINCH_KEY_ID") or "MY_KEY_ID"
key_secret = os.environ.get("SINCH_KEY_SECRET") or "MY_KEY_SECRET"
batch_id = os.environ.get("BATCH_ID") or "MY_BATCH_ID"

sinch_client = SinchClient(
    project_id=project_id,
    key_id=key_id,
    key_secret=key_secret,
)

# Poll the batch summary every 5s until all call sessions reach a final state,
# giving up after 60 checks (about 5 minutes)
interval_seconds, max_attempts = 5, 60
finished = False
for _ in range(max_attempts):
    response = sinch_client.voice.v2.batches.get(batch_id=batch_id)

    print(response)

    if response.queued == 0 and response.in_progress == 0:
        print("All call sessions finished.")
        finished = True
        break

    time.sleep(interval_seconds)

if not finished:
    sys.exit(
        f"Batch {batch_id} did not finish "
        f"after {max_attempts} attempts"
    )
