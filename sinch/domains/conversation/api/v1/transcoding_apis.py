from typing import List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.conversation.api.v1.base import BaseConversation
from sinch.domains.conversation.api.v1.internal.transcoding_endpoints import (
    TranscodeMessageEndpoint,
)
from sinch.domains.conversation.models.v1.messages.types.app_message_dict import (
    AppMessageDict,
)
from sinch.domains.conversation.models.v1.transcoding.internal.transcode_message_request import (
    TranscodeMessageRequest,
)
from sinch.domains.conversation.models.v1.transcoding.response.transcode_message_response import (
    TranscodeMessageResponse,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class Transcoding(BaseConversation):
    def transcode_message(
        self,
        app_id: str,
        app_message: AppMessageDict,
        channels: List[ConversationChannelType],
        from_: UnsetOr[Optional[str]] = UNSET,
        to: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> TranscodeMessageResponse:
        """
        Transcodes the message from the Conversation API format to the channel-specific
        formats for the requested channels. No message is sent to the contact.

        :param app_id: (required) The ID of the app used to transcode the message.
        :type app_id: str
        :param app_message: (required) The message to be transcoded.
        :type app_message: AppMessageDict
        :param channels: (required) The list of channels for which the message shall be transcoded.
        :type channels: List[ConversationChannelType]
        :param from_: (optional) The sender of the message. Serialized as ``from``.
        :type from_: UnsetOr[Optional[str]]
        :param to: (optional) The recipient of the message.
        :type to: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: The message transcoded for each requested channel, keyed by channel name.
        :rtype: TranscodeMessageResponse

        For detailed documentation, visit https://developers.sinch.com/docs/conversation/.
        """
        request_data = TranscodeMessageRequest(
            app_id=app_id,
            app_message=app_message,
            channels=channels,
            **strip_unset({"from_": from_, "to": to}),
            **kwargs,
        )
        return self._request(TranscodeMessageEndpoint, request_data)
