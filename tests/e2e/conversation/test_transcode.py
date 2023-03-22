from sinch.domains.conversation.models.transcoding.responses import TranscodeConversationMessageResponse


def test_transcode_message(sinch_client_sync, app_id):
    transcode_message_response = sinch_client_sync.conversation.transcoding.transcode_message(
        app_id=app_id,
        app_message={
            "text_message": {
                "text": "This is a text message."
            }
        },
        channels=["TELEGRAM", "SMS"]
    )
    assert isinstance(transcode_message_response, TranscodeConversationMessageResponse)


async def test_transcode_message_async(sinch_client_async, app_id):
    transcode_message_response = await sinch_client_async.conversation.transcoding.transcode_message(
        app_id=app_id,
        app_message={
            "text_message": {
                "text": "This is a text message."
            }
        },
        channels=["TELEGRAM", "SMS"]
    )
    assert isinstance(transcode_message_response, TranscodeConversationMessageResponse)
