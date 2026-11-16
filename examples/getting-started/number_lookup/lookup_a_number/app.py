import os

from dotenv import load_dotenv

from sinch import SinchClient


def lookup_a_number(sinch_client: SinchClient):
    """Look up a number through the Number Lookup API."""
    # The phone number to lookup in E.164 format
    phone_number = "PHONE_NUMBER_TO_LOOKUP"

    response = sinch_client.number_lookup.lookup(
        number=phone_number,
    )

    print(f"Response: {response}")


load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID"),
    key_id=os.environ.get("SINCH_KEY_ID"),
    key_secret=os.environ.get("SINCH_KEY_SECRET"),
)

if __name__ == "__main__":
    lookup_a_number(sinch_client)
