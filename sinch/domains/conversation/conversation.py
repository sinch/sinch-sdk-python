from sinch.domains.conversation.api.v1 import (
    Messages,
)
from sinch.domains.conversation.sinch_events.v1 import ConversationSinchEvent


class Conversation:
    """
    Documentation for Sinch Conversation is found at
    https://developers.sinch.com/docs/conversation/.
    """

    def __init__(self, sinch):
        self._sinch = sinch
        self.messages = Messages(self._sinch)

    def sinch_events(
        self, callback_secret: str = ""
    ) -> ConversationSinchEvent:
        """
        Create a Conversation API Sinch Events handler with the given callback secret.

        :param callback_secret: Secret used for Sinch Event signature validation.
        :type callback_secret: str
        :returns: A configured Sinch Events handler.
        :rtype: ConversationSinchEvent
        """
        return ConversationSinchEvent(callback_secret)
