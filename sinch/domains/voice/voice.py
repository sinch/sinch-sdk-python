from sinch.domains.voice.api.v2.voice import VoiceV2


class Voice:
    """
    Documentation for Sinch Voice is found at
    https://developers.sinch.com/docs/voice/.
    """

    def __init__(self, sinch):
        self._sinch = sinch
        self.v2 = VoiceV2(self._sinch)