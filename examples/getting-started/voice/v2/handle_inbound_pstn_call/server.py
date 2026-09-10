import logging

from config import config
from controller import VoiceController
from flask import Flask

from sinch import SinchClient

app = Flask(__name__)

port = int(config.get("SERVER_PORT") or "3001")

sinch_client = SinchClient(
    project_id=config.get("SINCH_PROJECT_ID", ""),
    key_id=config.get("SINCH_KEY_ID", ""),
    key_secret=config.get("SINCH_KEY_SECRET", ""),
)
logging.basicConfig()
sinch_client.configuration.logger.setLevel(logging.INFO)

conversation_controller = VoiceController(sinch_client)

app.add_url_rule(
    "/VoiceSinchEvent",
    methods=["POST"],
    view_func=conversation_controller.voice_event,
)

if __name__ == "__main__":
    print("Getting Started: Handle Inbound PSTN Call")
    print(f"Listening on port {port}. Expose with: ngrok http {port}")
    app.run(port=port)
