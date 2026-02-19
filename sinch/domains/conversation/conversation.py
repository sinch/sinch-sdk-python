from sinch.domains.conversation.api.v1 import (
    Messages,
)
from sinch.domains.conversation.webhooks.v1 import ConversationWebhooks


class Conversation:
    """
    Documentation for Sinch Conversation is found at
    https://developers.sinch.com/docs/conversation/.
    """

    def __init__(self, sinch):
        self._sinch = sinch
        self.messages = Messages(self._sinch)

    def webhooks(self, callback_secret: str) -> ConversationWebhooks:
        """
        Create a Conversation API webhooks handler with the given webhook secret.

        :param callback_secret: Secret used for webhook signature validation.
        :type callback_secret: str
        :returns: A configured webhooks handler.
        :rtype: ConversationWebhooks
        """
        return ConversationWebhooks(callback_secret)
