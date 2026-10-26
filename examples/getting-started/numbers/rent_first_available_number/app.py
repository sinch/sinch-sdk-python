import os

from dotenv import load_dotenv

from sinch import SinchClient


def rent_first_available_number(sinch_client: SinchClient):
    """Rent the first available virtual number through the Numbers API."""
    service_plan_id_to_associate_with_the_number = "MY_SERVICE_PLAN_ID"

    response = sinch_client.numbers.rent_any(
        region_code="US",
        number_type="LOCAL",
        sms_configuration={
            "service_plan_id": service_plan_id_to_associate_with_the_number,
        },
    )

    print(f"Response: {response}")


load_dotenv()

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID"),
    key_id=os.environ.get("SINCH_KEY_ID"),
    key_secret=os.environ.get("SINCH_KEY_SECRET"),
)

if __name__ == "__main__":
    rent_first_available_number(sinch_client)
