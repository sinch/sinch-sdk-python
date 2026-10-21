from sinch.domains.conversation.api.v1 import (
    Apps,
    Capability,
    Consents,
    Contacts,
    Conversations,
    EventDestinations,
    Events,
    Messages,
    ProjectSettings,
    Transcoding,
)
from sinch.domains.conversation.sinch_events.v1 import ConversationSinchEvent
from sinch.domains.conversation.templates.api.v2.templates_apis import (
    Templates,
)


class Conversation:
    """
    Documentation for Sinch Conversation is found at
    https://developers.sinch.com/docs/conversation/.
    """

    def __init__(self, sinch):
        self._sinch = sinch
        self.apps = Apps(sinch)
        self.capability = Capability(self._sinch)
        self.consents = Consents(self._sinch)
        self.contacts = Contacts(self._sinch)
        self.conversations = Conversations(self._sinch)
        self.event_destinations = EventDestinations(self._sinch)
        self.events = Events(self._sinch)
        self.messages = Messages(self._sinch)
        self.project_settings = ProjectSettings(self._sinch)
        self.transcoding = Transcoding(self._sinch)
        self.templates = Templates(self._sinch)

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
