import logging
from pathlib import Path


from flask import Flask, request
from dotenv import dotenv_values

from sinch import SinchClient
from controller import ConversationController

app = Flask(__name__)


def load_config():
    current_dir = Path(__file__).resolve().parent
    env_file = current_dir / ".env"
    if not env_file.exists():
        raise FileNotFoundError(f"Missing .env in {current_dir}. Copy from .env.example.")
    return dict(dotenv_values(env_file))


config = load_config()
port = int(config.get("SERVER_PORT") or "3001")
app_id = config.get("CONVERSATION_APP_ID") or ""
webhooks_secret = config.get("CONVERSATION_WEBHOOKS_SECRET") or ""

sinch_client = SinchClient(
    project_id=config.get("SINCH_PROJECT_ID", ""),
    key_id=config.get("SINCH_KEY_ID", ""),
    key_secret=config.get("SINCH_KEY_SECRET", ""),
    conversation_region=config.get("SINCH_CONVERSATION_REGION", "eu"),
)
logging.basicConfig()
sinch_client.configuration.logger.setLevel(logging.INFO)

conversation_controller = ConversationController(
    sinch_client, webhooks_secret, app_id
)


@app.before_request
def before_request():
    request.raw_body = request.get_data()


app.add_url_rule(
    "/ConversationEvent",
    methods=["POST"],
    view_func=conversation_controller.conversation_event,
)

if __name__ == "__main__":
    print("Getting Started: MO SMS → MT reply (Conversation API, DISPATCH, channel identity)")
    print(f"App ID: {app_id or '(set CONVERSATION_APP_ID in .env)'}")
    print(f"Listening on port {port}. Expose with: ngrok http {port}")
    app.run(port=port)
