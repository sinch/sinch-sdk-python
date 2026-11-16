import os

from dotenv import load_dotenv

from sinch import SinchClient


def rent_and_configure(sinch_client: SinchClient):
    """Rent a specific virtual number through the Numbers API."""
    # Available numbers list can be retrieved by using search_for_available_numbers()
    # function from Numbers service, see:
    # https://developers.sinch.com/docs/numbers/getting-started
    phone_number_to_be_rented = "AVAILABLE_PHONE_NUMBER_TO_BE_RENTED"
    service_plan_id_to_associate_with_the_number = "MY_SERVICE_PLAN_ID"

    response = sinch_client.numbers.rent(
        phone_number=phone_number_to_be_rented,
        sms_configuration={
            "service_plan_id": service_plan_id_to_associate_with_the_number,
        },
    )

    print(f"Successfully rented number: {response.phone_number}")


load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID"),
    key_id=os.environ.get("SINCH_KEY_ID"),
    key_secret=os.environ.get("SINCH_KEY_SECRET"),
)

if __name__ == "__main__":
    rent_and_configure(sinch_client)
