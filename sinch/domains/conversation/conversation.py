from sinch.domains.conversation.api.v1 import (
    Messages,
)


class Conversation:
    """
    Documentation for Sinch Conversation is found at
    https://developers.sinch.com/docs/conversation/.
    """

    def __init__(self, sinch):
        self._sinch = sinch
        self.messages = Messages(self._sinch)
