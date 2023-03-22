from flask import Flask
from sinch import Sinch
from sinch.domains.conversation.models.app.requests import SinchCreateConversationApp
from sinch.domains.conversation.models import (
    SinchConversationTelegramCredentials,
    SinchConversationChannelCredentials
)
from sinch.domains.conversation.enums import ConversationChannel

"""
Run with: export FLASK_APP=flask_example.py; flask run
"""

app = Flask("Sinch_example")
sinch_client = Sinch(key_id="killer", key_secret="rabbit")


@app.route("/project")
def project():
    telegram_credentials = SinchConversationChannelCredentials(
        channel=ConversationChannel.TELEGRAM.value,
        telegram_credentials=SinchConversationTelegramCredentials(token="Knights of Ni!")
    )

    sinch_app = SinchCreateConversationApp(
        project_id="SpanishInquisition",
        display_name="NobodyExpected",
        channel_credentials=telegram_credentials
    ).as_dict()

    sinch_client.conversation.create_app(**sinch_app)
    return {"sinch_app_id": sinch_app.id}
