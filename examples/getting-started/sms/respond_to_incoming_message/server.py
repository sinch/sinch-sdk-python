import logging
import os

from controller import SmsController
from dotenv import load_dotenv
from flask import Flask

from sinch import SinchClient

load_dotenv()

app = Flask(__name__)
port = int(os.environ.get("SERVER_PORT") or 3001)

sinch_client = SinchClient(
    project_id=os.environ.get("SINCH_PROJECT_ID"),
    key_id=os.environ.get("SINCH_KEY_ID"),
    key_secret=os.environ.get("SINCH_KEY_SECRET"),
    sms_region=os.environ.get("SINCH_SMS_REGION"),
    service_plan_id=os.environ.get("SINCH_SERVICE_PLAN_ID"),
    sms_api_token=os.environ.get("SINCH_API_TOKEN"),
)
logging.basicConfig()
sinch_client.configuration.logger.setLevel(logging.INFO)

sms_controller = SmsController(sinch_client)

app.add_url_rule(
    "/SmsEvent",
    methods=["POST"],
    view_func=sms_controller.sms_event,
)

if __name__ == "__main__":
    print(f"Server is listening on port {port}")
    app.run(port=port)
