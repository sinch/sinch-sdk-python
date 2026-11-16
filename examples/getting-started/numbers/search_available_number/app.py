import os

from dotenv import load_dotenv

from sinch import SinchClient


def search_available_number(sinch_client: SinchClient):
    """Search for available virtual numbers through the Numbers API."""
    region_code = "US"
    number_type = "LOCAL"

    response = sinch_client.numbers.search_for_available_numbers(
        region_code=region_code,
        number_type=number_type,
    )

    for number in response.iterator():
        print(f"Available number: {number}")


load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID"),
    key_id=os.environ.get("SINCH_KEY_ID"),
    key_secret=os.environ.get("SINCH_KEY_SECRET"),
)

if __name__ == "__main__":
    search_available_number(sinch_client)
