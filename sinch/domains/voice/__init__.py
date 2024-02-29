from sinch.domains.voice.endpoints.callouts.callout import CalloutEndpoint
from sinch.domains.voice.endpoints.calls.get_call import GetCallEndpoint
from sinch.domains.voice.endpoints.calls.update_call import UpdateCallEndpoint
from sinch.domains.voice.endpoints.calls.manage_call import ManageCallEndpoint

from sinch.domains.voice.endpoints.applications.get_numbers import GetVoiceNumbersEndpoint
from sinch.domains.voice.endpoints.applications.query_number import QueryVoiceNumberEndpoint
from sinch.domains.voice.endpoints.applications.get_callback_urls import GetVoiceCallbacksEndpoint
from sinch.domains.voice.endpoints.applications.unassign_number import UnAssignVoiceNumberEndpoint

from sinch.domains.voice.endpoints.conferences.kick_participant import KickParticipantConferenceEndpoint
from sinch.domains.voice.endpoints.conferences.kick_all_participants import KickAllConferenceEndpoint
from sinch.domains.voice.endpoints.conferences.manage_participant import ManageParticipantConferenceEndpoint
from sinch.domains.voice.endpoints.conferences.get_conference import GetConferenceEndpoint

from sinch.domains.voice.enums import CalloutMethod
from sinch.domains.voice.models.callouts.responses import VoiceCalloutResponse
from sinch.domains.voice.models.callouts.requests import (
    ConferenceVoiceCalloutRequest,
    TextToSpeechVoiceCalloutRequest,
    CustomVoiceCalloutRequest
)
from sinch.domains.voice.models.calls.requests import (
    GetVoiceCallRequest,
    UpdateVoiceCallRequest,
    ManageVoiceCallRequest
)
from sinch.domains.voice.models.calls.responses import (
    GetVoiceCallResponse,
    UpdateVoiceCallResponse,
    ManageVoiceCallResponse
)
from sinch.domains.voice.models.conferences.requests import (
    GetVoiceConferenceRequest,
    KickAllVoiceConferenceRequest,
    KickParticipantVoiceConferenceRequest,
    ManageParticipantVoiceConferenceRequest
)
from sinch.domains.voice.models.conferences.responses import (
    GetVoiceConferenceResponse,
    KickAllVoiceConferenceResponse,
    ManageParticipantVoiceConferenceResponse,
    KickParticipantVoiceConferenceResponse
)
from sinch.domains.voice.models.applications.requests import (
    GetNumbersVoiceApplicationRequest,
    AssignNumbersVoiceApplicationRequest,
    UnassignNumbersVoiceApplicationRequest,
    GetCallbackUrlsVoiceApplicationRequest,
    QueryNumberVoiceApplicationRequest
)
from sinch.domains.voice.models.applications.responses import (
    GetNumbersVoiceApplicationResponse,
    AssignNumbersVoiceApplicationResponse,
    UnassignNumbersVoiceApplicationResponse,
    KickParticipantVoiceConferenceResponse,
    GetCallbackUrlsVoiceApplicationResponse,
    QueryNumberVoiceApplicationResponse
)


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
    ) -> VoiceCalloutResponse:
        return self._sinch.configuration.transport.request(
            CalloutEndpoint(
                callout_method=CalloutMethod.TEXT_TO_SPEECH.value,
                request_data=TextToSpeechVoiceCalloutRequest(
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
    ) -> VoiceCalloutResponse:
        return self._sinch.configuration.transport.request(
            CalloutEndpoint(
                callout_method=CalloutMethod.CONFERENCE.value,
                request_data=ConferenceVoiceCalloutRequest(
                    destination=destination,
                    conferenceId=conference_id,
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
    ) -> VoiceCalloutResponse:
        return self._sinch.configuration.transport.request(
            CalloutEndpoint(
                callout_method=CalloutMethod.CUSTOM.value,
                request_data=CustomVoiceCalloutRequest(
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
                    call_id=call_id
                )
            )
        )

    def update(
        self,
        call_id: str,
        instructions: list,
        action: dict
    ) -> UpdateVoiceCallResponse:
        return self._sinch.configuration.transport.request(
            UpdateCallEndpoint(
                request_data=UpdateVoiceCallRequest(
                    call_id=call_id,
                    instructions=instructions,
                    action=action
                )
            )
        )

    def manage(
        self,
        call_id: str,
        call_leg: str,
        instructions: list,
        action: dict
    ) -> ManageVoiceCallResponse:
        return self._sinch.configuration.transport.request(
            ManageCallEndpoint(
                request_data=ManageVoiceCallRequest(
                    call_id=call_id,
                    call_leg=call_leg,
                    instructions=instructions,
                    action=action
                )
            )
        )


class Conferences:
    def __init__(self, sinch):
        self._sinch = sinch

    def get(self, conference_id: str) -> GetVoiceConferenceResponse:
        return self._sinch.configuration.transport.request(
            GetConferenceEndpoint(
                request_data=GetVoiceConferenceRequest(
                    conference_id=conference_id
                )
            )
        )

    def kick_all(self, conference_id: str) -> KickAllVoiceConferenceResponse:
        return self._sinch.configuration.transport.request(
            KickAllConferenceEndpoint(
                request_data=KickAllVoiceConferenceRequest(
                    conference_id=conference_id
                )
            )
        )

    def kick_participant(
        self,
        call_id: str,
        conference_id: str,
    ) -> KickParticipantVoiceConferenceResponse:
        return self._sinch.configuration.transport.request(
            KickParticipantConferenceEndpoint(
                request_data=KickParticipantVoiceConferenceRequest(
                    call_id=call_id,
                    conference_id=conference_id
                )
            )
        )

    def manage_participant(
        self,
        call_id: str,
        conference_id: str,
        command: str,
        moh: str = None
    ) -> ManageParticipantVoiceConferenceResponse:
        return self._sinch.configuration.transport.request(
            ManageParticipantConferenceEndpoint(
                request_data=ManageParticipantVoiceConferenceRequest(
                    call_id=call_id,
                    conference_id=conference_id,
                    command=command,
                    moh=moh
                )
            )
        )


class Applications:
    def __init__(self, sinch):
        self._sinch = sinch

    def get_numbers(self) -> GetNumbersVoiceApplicationResponse:
        return self._sinch.configuration.transport.request(
            GetVoiceNumbersEndpoint()
        )

    def assign_numbers(self, call_id) -> AssignNumbersVoiceApplicationResponse:
        return self._sinch.configuration.transport.request(
            AssignVoiceNumbersEndxpoint(
                request_data=AssignNumbersVoiceApplicationRequest(
                    call_id=call_id
                )
            )
        )

    def unassign_number(
        self,
        number: str,
        application_key: str =None,
        capability: str = None

    ) -> UnassignNumbersVoiceApplicationResponse:
        return self._sinch.configuration.transport.request(
            UnAssignVoiceNumberEndpoint(
                request_data=UnassignNumbersVoiceApplicationRequest(
                    number=number,
                    application_key=application_key,
                    capability=capability
                )
            )
        )

    def get_callback_urls(self) -> GetCallbackUrlsVoiceApplicationResponse:
        return self._sinch.configuration.transport.request(
            GetVoiceCallbacksEndpoint()
        )

    def query_number(self, number) -> QueryNumberVoiceApplicationResponse:
        return self._sinch.configuration.transport.request(
            QueryVoiceNumberEndpoint(
                request_data=QueryNumberVoiceApplicationRequest(
                    number=number
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
        self.conferences = Conferences(self._sinch)
        self.applications = Applications(self._sinch)


class VoiceAsync(VoiceBase):
    """
    Asynchronous version of the Voice Domain
    """
    __doc__ += VoiceBase.__doc__

    def __init__(self, sinch):
        super().__init__(sinch)
        self.callouts = Callouts(self._sinch)
        self.calls = Calls(self._sinch)
        self.conferences = Conferences(self._sinch)
        self.applications = Applications(self._sinch)
