import os

from dotenv import load_dotenv

from sinch import SinchClient


def send_text_message(sinch_client: SinchClient):
    """Send a demo SMS message through the Conversation API."""
    app_id = "CONVERSATION_APPLICATION_ID"
    from_number = "SINCH_VIRTUAL_PHONE_NUMBER"
    to_number = "RECIPIENT_PHONE_NUMBER"

    body = (
        "This is a test Conversation message sent using the Sinch Python SDK."
    )

    response = sinch_client.conversation.messages.send_text_message(
        app_id=app_id,
        text=body,
        recipient_identities=[
            {
                "channel": "SMS",
                "identity": to_number,
            }
        ],
        channel_properties={
            "SMS_SENDER": from_number,
        },
    )

    print(f"Response: {response}")


load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID"),
    key_id=os.environ.get("SINCH_KEY_ID"),
    key_secret=os.environ.get("SINCH_KEY_SECRET"),
    conversation_region=os.environ.get("SINCH_CONVERSATION_REGION"),
)

if __name__ == "__main__":
    send_text_message(sinch_client)
