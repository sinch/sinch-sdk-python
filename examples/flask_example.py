import os
from flask import Flask
from sinch import SinchClient
from sinch.domains.conversation.enums import ConversationChannel

"""
Run with: export FLASK_APP=flask_example.py; flask run
"""

app = Flask("Sinch_example")

sinch_client = SinchClient(
    key_id=os.getenv("KEY_ID"),
    key_secret=os.getenv("KEY_SECRET"),
    project_id=os.getenv("PROJECT_ID")
)


@app.route("/create_app", methods=['POST'])
def project():
    conversation_api_app = sinch_client.conversation.app.create(
        display_name="Shrubbery",
        channel_credentials=[
            {
                "channel": ConversationChannel.TELEGRAM.value,
                "telegram_credentials": {
                    "token": "herring"
                }
            }
        ],
        retention_policy={
            "ttl_days": 20,
            "retention_type": "MESSAGE_EXPIRE_POLICY"
        }
    )
    return {"sinch_app_id": conversation_api_app.id}
