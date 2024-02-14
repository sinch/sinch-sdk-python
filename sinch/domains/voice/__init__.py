from sinch.domains.voice.endpoints.callouts.callout import CalloutEndpoint
from sinch.domains.voice.endpoints.calls.get_call import GetCallEndpoint
from sinch.domains.voice.endpoints.calls.update_call import UpdateCallEndpoint
from sinch.domains.voice.enums import CalloutMethod
from sinch.domains.voice.models.callouts.responses import CalloutResponse
from sinch.domains.voice.models.callouts.requests import (
    ConferenceCalloutRequest,
    TextToSpeechCalloutRequest,
    CustomCalloutRequest
)
from sinch.domains.voice.models.calls.requests import GetVoiceCallRequest, UpdateVoiceCallRequest
from sinch.domains.voice.models.calls.responses import GetVoiceCallResponse


class Callouts:
    def __init__(self, sinch):
        self._sinch = sinch

    def text_to_speech(
        self,
        destination: dict,
        cli: str = None,
        dtmf: str = None,
        domain: str = None,
        custom: str = None,
        locale: str = None,
        text: str = None,
        prompts: str = None,
        enable_ace: bool = None,
        enable_dice: bool = None,
        enable_pie: bool = None
    ) -> CalloutResponse:
        return self._sinch.configuration.transport.request(
            CalloutEndpoint(
                callout_method=CalloutMethod.TTS.value,
                request_data=TextToSpeechCalloutRequest(
                    destination=destination,
                    cli=cli,
                    dtmf=dtmf,
                    domain=domain,
                    custom=custom,
                    locale=locale,
                    text=text,
                    prompts=prompts,
                    enableAce=enable_ace,
                    enableDice=enable_dice,
                    enablePie=enable_pie
                )
            )
        )

    def conference(
        self,
        destination: dict,
        conference_id: str,
        cli: str = None,
        conference_dtmf_options: dict = None,
        dtmf: str = None,
        conference: str = None,
        max_duration: int = None,
        enable_ace: bool = None,
        enable_dice: bool = None,
        enable_pie: bool = None,
        locale: str = None,
        greeting: str = None,
        moh_class: str = None,
        custom: str = None,
        domain: str = None
    ) -> CalloutResponse:
        return self._sinch.configuration.transport.request(
            CalloutEndpoint(
                callout_method=CalloutMethod.CONFERENCE.value,
                request_data=ConferenceCalloutRequest(
                    destination=destination,
                    conference_id=conference_id,
                    cli=cli,
                    conferenceDtmfOptions=conference_dtmf_options,
                    dtmf=dtmf,
                    conference=conference,
                    maxDuration=max_duration,
                    enableAce=enable_ace,
                    enableDice=enable_dice,
                    enablePie=enable_pie,
                    locale=locale,
                    greeting=greeting,
                    mohClass=moh_class,
                    custom=custom,
                    domain=domain
                )
            )
        )

    def custom(
        self,
        cli: str = None,
        destination: dict = None,
        dtmf: str = None,
        custom: str = None,
        max_duration: int = None,
        ice: str = None,
        ace: str = None,
        pie: str = None
    ) -> CalloutResponse:
        return self._sinch.configuration.transport.request(
            CalloutEndpoint(
                callout_method=CalloutMethod.CUSTOM.value,
                request_data=CustomCalloutRequest(
                    cli=cli,
                    destination=destination,
                    dtmf=dtmf,
                    custom=custom,
                    maxDuration=max_duration,
                    ice=ice,
                    ace=ace,
                    pie=pie
                )
            )
        )


class Calls:
    def __init__(self, sinch):
        self._sinch = sinch

    def get(self, call_id) -> GetVoiceCallResponse:
        return self._sinch.configuration.transport.request(
            GetCallEndpoint(
                request_data=GetVoiceCallRequest(
                    callId=call_id
                )
            )
        )

    def update(
        self,
        call_id,
        instructions: list,
        action: dict
    ):
        return self._sinch.configuration.transport.request(
            UpdateCallEndpoint(
                request_data=UpdateVoiceCallRequest(
                    callId=call_id,
                    instructions=instructions,
                    action=action
                )
            )
        )


class VoiceBase:
    """
    Documentation for the Voice API: https://developers.sinch.com/docs/voice/
    """
    def __init__(self, sinch):
        self._sinch = sinch


class Voice(VoiceBase):
    """
    Synchronous version of the Voice Domain
    """
    __doc__ += VoiceBase.__doc__

    def __init__(self, sinch):
        super().__init__(sinch)
        self.callouts = Callouts(self._sinch)
        self.calls = Calls(self._sinch)


class VoiceAsync(VoiceBase):
    """
    Asynchronous version of the Voice Domain
    """
    __doc__ += VoiceBase.__doc__

    def __init__(self, sinch):
        super().__init__(sinch)
        self.callouts = Callouts(self._sinch)
        self.calls = Calls(self._sinch)
