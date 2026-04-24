import logging

from flask import Flask, request
from numbers_api.controller import NumbersController
from sms_api.controller import SmsController
from conversation_api.controller import ConversationController
from sinch_client_helper import get_sinch_client, load_config

app = Flask(__name__)

config = load_config()
port = int(config.get('SERVER_PORT') or 3001)
numbers_sinch_event_secret = config.get('NUMBERS_SINCH_EVENT_SECRET')
sms_sinch_event_secret = config.get('SMS_SINCH_EVENT_SECRET')
conversation_sinch_event_secret = config.get('CONVERSATION_SINCH_EVENT_SECRET')
sinch_client = get_sinch_client(config)

# Set up logging at the INFO level
logging.basicConfig()
sinch_client.configuration.logger.setLevel(logging.INFO)

numbers_controller = NumbersController(sinch_client, numbers_sinch_event_secret)
sms_controller = SmsController(sinch_client, sms_sinch_event_secret)
conversation_controller = ConversationController(
    sinch_client, conversation_sinch_event_secret or ''
)


# Middleware to capture raw body
@app.before_request
def before_request():
    request.raw_body = request.get_data()


app.add_url_rule('/NumbersEvent', methods=['POST'], view_func=numbers_controller.numbers_event)
app.add_url_rule('/SmsEvent', methods=['POST'], view_func=sms_controller.sms_event)
app.add_url_rule('/ConversationEvent', methods=['POST'], view_func=conversation_controller.conversation_event)

if __name__ == '__main__':
    app.run(port=port)
