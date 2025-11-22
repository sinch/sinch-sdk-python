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

delivery_reports = sinch_client.sms.delivery_reports.list(
    page=0,
    page_size=10
)

page_counter = 1
reached_last_page = False

while not reached_last_page:
    print(f"Page {page_counter} List of Delivery Reports: {delivery_reports}")

    if delivery_reports.has_next_page:
        delivery_reports = delivery_reports.next_page()
        page_counter += 1
    else:
        reached_last_page = True
