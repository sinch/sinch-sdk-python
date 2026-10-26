import os

from dotenv import load_dotenv

from sinch import SinchClient


def send_sms_message(sinch_client: SinchClient):
    """Send a demo SMS message through the SMS API."""
    sender = "SENDER_NUMBER"
    recipient = "RECIPIENT_PHONE_NUMBER"
    body = "This is a test SMS message using the Sinch Python SDK."

    response = sinch_client.sms.batches.send_sms(
        from_=sender,
        to=[recipient],
        body=body,
    )

    print(f"Response: {response}")


load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID"),
    key_id=os.environ.get("SINCH_KEY_ID"),
    key_secret=os.environ.get("SINCH_KEY_SECRET"),
    sms_region=os.environ.get("SINCH_SMS_REGION"),
    service_plan_id=os.environ.get("SINCH_SERVICE_PLAN_ID"),
    sms_api_token=os.environ.get("SINCH_API_TOKEN"),
)

if __name__ == "__main__":
    send_sms_message(sinch_client)
