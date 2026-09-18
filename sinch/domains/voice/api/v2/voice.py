from sinch.domains.voice.api.v2.batches_apis import Batches
from sinch.domains.voice.api.v2.calls_apis import Calls
from sinch.domains.voice.api.v2.services_apis import Services
from sinch.domains.voice.api.v2.sessions_apis import Sessions
from sinch.domains.voice.api.v2.sinch_events import SinchEvents
from sinch.domains.voice.api.v2.svaml_apis import Svaml


class VoiceV2:
    """Version 2 of the Sinch Voice API."""

    def __init__(self, sinch):
        self._sinch = sinch
        self.calls = Calls(self._sinch)
        self.sessions = Sessions(self._sinch)
        self.batches = Batches(self._sinch)
        self.services = Services(self._sinch)
        self.svaml = Svaml(self._sinch)
        self.sinch_events = SinchEvents()
