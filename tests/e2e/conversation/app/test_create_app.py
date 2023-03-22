from sinch.domains.conversation.models.app.responses import CreateConversationAppResponse
from sinch.domains.conversation.models import SinchConversationTelegramCredentials, SinchConversationChannelCredentials
from sinch.domains.conversation.enums import ConversationRetentionPolicyType, ConversationChannel


def test_create_app(sinch_client_sync):
    create_app_response = sinch_client_sync.conversation.app.create(
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
            "retention_type": ConversationRetentionPolicyType.MESSAGE_EXPIRE_POLICY.value
        }
    )
    assert isinstance(create_app_response, CreateConversationAppResponse)


async def test_create_app_using_dataclass(sinch_client_async):
    telegram_credentials = SinchConversationChannelCredentials(
        channel=ConversationChannel.TELEGRAM.value,
        telegram_credentials=SinchConversationTelegramCredentials(token="Knights of Ni!")
    )

    new_sinch_app = {
        "display_name": "Dataclass",
        "channel_credentials": [telegram_credentials]
    }

    create_app_response = await sinch_client_async.conversation.app.create(**new_sinch_app)
    assert isinstance(create_app_response, CreateConversationAppResponse)
