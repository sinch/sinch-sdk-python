import logging
import sys
from pathlib import Path

# Add examples directory to Python path to allow importing sinch_events
examples_dir = Path(__file__).resolve().parent.parent
if str(examples_dir) not in sys.path:
    sys.path.insert(0, str(examples_dir))

from flask import Flask, request
from sinch_events.numbers_api.controller import NumbersController
from sinch_events.sms_api.controller import SmsController
from sinch_events.conversation_api.controller import ConversationController
from sinch_events.sinch_client_helper import get_sinch_client, load_config

app = Flask(__name__)

config = load_config()
port = int(config.get('SERVER_PORT') or 3001)
numbers_webhooks_secret = config.get('NUMBERS_WEBHOOKS_SECRET')
sms_sinch_event_secret = config.get('SMS_WEBHOOKS_SECRET')
conversation_webhooks_secret = config.get('CONVERSATION_WEBHOOKS_SECRET')
sinch_client = get_sinch_client(config)

# Set up logging at the INFO level
logging.basicConfig()
sinch_client.configuration.logger.setLevel(logging.INFO)

numbers_controller = NumbersController(sinch_client, numbers_webhooks_secret)
sms_controller = SmsController(sinch_client, sms_sinch_event_secret)
conversation_controller = ConversationController(sinch_client, conversation_webhooks_secret or '')


# Middleware to capture raw body
@app.before_request
def before_request():
    request.raw_body = request.get_data()


app.add_url_rule('/NumbersEvent', methods=['POST'], view_func=numbers_controller.numbers_event)
app.add_url_rule('/SmsEvent', methods=['POST'], view_func=sms_controller.sms_event)
app.add_url_rule('/ConversationEvent', methods=['POST'], view_func=conversation_controller.conversation_event)

if __name__ == '__main__':
    app.run(port=port)
