from sinch.domains.voice.api.v2.calls_apis import Calls


class VoiceV2:
    """Version 2 of the Sinch Voice API."""

    def __init__(self, sinch):
        self._sinch = sinch
        self.calls = Calls(self._sinch)
