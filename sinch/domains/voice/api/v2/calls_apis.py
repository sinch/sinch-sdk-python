from datetime import datetime
from typing import List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.pagination import LinkBasedPaginator, Paginator
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.api.v2.base.base_voice import BaseVoice
from sinch.domains.voice.api.v2.internal.calls_endpoints import (
    GetCallByIdEndpoint,
    ListCallsEndpoint,
    PatchCallByIdEndpoint,
    PatchCallBySessionAndNameEndpoint,
    StartCallEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.list_calls_response import (
    ListCallsResponse,
)
from sinch.domains.voice.models.v2.calls.internal.request.call_id_request import (
    CallIdRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.list_calls_request import (
    ListCallsRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_id_request import (
    PatchCallByIdRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_session_and_name_request import (
    PatchCallBySessionAndNameRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call
from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
    SvamlCommandDict,
)
from sinch.domains.voice.models.v2.types.call_reason import CallReason
from sinch.domains.voice.models.v2.types.call_result import CallResult
from sinch.domains.voice.models.v2.types.call_type import CallType


class Calls(BaseVoice):
    def start(
        self,
        commands: List[SvamlCommandDict],
        service_id: Optional[str] = None,
        idempotency_key: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> StartCallResponse:
        """
        Create a new outbound call, associated to the project's default service or to the service specified in the `serviceId` query parameter.

        :param commands: (required) SVAML commands describing the call flow.
        :type commands: List[SvamlCommandDict]
        :param service_id: (optional) The ID of the service to use for the call. If omitted, the project's default service is used.
        :type service_id: Optional[str]
        :param idempotency_key: (optional) Client-generated idempotency key to safely retry requests. If a request with the same key is received within 10 minutes, the cached response from the original request is returned. Using a random UUID (v4) is strongly recommended.
        :type idempotency_key: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The created call session.
        :rtype: StartCallResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        request_data = StartCallRequest(
            commands=commands,
            service_id=service_id,
            **strip_unset(
                {
                    "idempotency_key": idempotency_key,
                }
            ),
            **kwargs,
        )
        return self._request(StartCallEndpoint, request_data)

    def list(
        self,
        service_id: Optional[str] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        call_type: Optional[CallType] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        call_result: Optional[CallResult] = None,
        call_reason: Optional[CallReason] = None,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs,
    ) -> Paginator[ListCallsResponse, Call]:
        """
        List and filter calls made with Sinch

        :param service_id: (optional) The ID of the service.
        :type service_id: Optional[str]
        :param from_: (optional) Only include calls where `from` matches this origin. For inbound calls, this is the caller; for outbound calls, this is the calling party.
        :type from_: Optional[str]
        :param to: (optional) Only include calls where `to` matches this destination. For inbound calls, this is the called party; for outbound calls, this is the callee/recipient.
        :type to: Optional[str]
        :param call_type: (optional) Only include calls of the specified type. If omitted, calls of all types are included.
        :type call_type: Optional[CallType]
        :param start_time: (optional) Only include calls that started at or after this timestamp.
        :type start_time: Optional[datetime]
        :param end_time: (optional) Only include calls that ended before this timestamp (exclusive).
        :type end_time: Optional[datetime]
        :param call_result: (optional) Filter results to only include calls whose call result matches the specified value. If omitted, calls with any result are included.
        :type call_result: Optional[CallResult]
        :param call_reason: (optional) Filter results to only include calls whose call reason matches the specified value. If omitted, calls with any reason are included.
        :type call_reason: Optional[CallReason]
        :param page_size: (optional) Number of items to be returned on each page.
        :type page_size: Optional[int]
        :param page: (optional) Page number (1-based).
        :type page: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: LinkBasedPaginator with Call items
        :rtype: Paginator[ListCallsResponse,Call]

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        return LinkBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListCallsEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListCallsRequest(
                    service_id=service_id,
                    from_=from_,
                    to=to,
                    call_type=call_type,
                    start_time=start_time,
                    end_time=end_time,
                    call_result=call_result,
                    call_reason=call_reason,
                    page_size=page_size,
                    page=page,
                    **kwargs,
                ),
            ),
        )

    def get(self, call_id: str, **kwargs) -> Call:
        """
        Retrieve detailed information about a specific call using its unique identifier.

        :param call_id: (required) The ID of the call.
        :type call_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The call details.
        :rtype: Call

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        request_data = CallIdRequest(call_id=call_id, **kwargs)
        return self._request(GetCallByIdEndpoint, request_data)

    def interact_by_call_id(
        self,
        call_id: str,
        commands: List[SvamlCommandDict],
        idempotency_key: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> None:
        """
        Interact with an ongoing call by submitting a set of SVAML commands. Use this to force disconnect, play messages, bridge with another call, or perform other call control actions.

        :param call_id: (required) The ID of the call.
        :type call_id: str
        :param commands: (required) SVAML commands describing the call flow.
        :type commands: List[SvamlCommandDict]
        :param idempotency_key: (optional) Client-generated idempotency key to safely retry requests. If a request with the same key is received within 10 minutes, the cached response from the original request is returned. Using a random UUID (v4) is strongly recommended.
        :type idempotency_key: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        request_data = PatchCallByIdRequest(
            call_id=call_id,
            commands=commands,
            **strip_unset(
                {
                    "idempotency_key": idempotency_key,
                }
            ),
            **kwargs,
        )
        return self._request(PatchCallByIdEndpoint, request_data)

    def interact_by_call_name(
        self,
        session_id: str,
        call_name: str,
        commands: List[SvamlCommandDict],
        idempotency_key: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> None:
        """
        Interact with an ongoing call identified by its session and call name by submitting a set of SVAML commands. Use this to force disconnect, play messages, bridge with another call, or perform other call control actions.

        :param session_id: (required) The ID of the session.
        :type session_id: str
        :param call_name: (required) The name of the call leg within the session, as assigned by the `callName` property in the `dial` command.
        :type call_name: str
        :param commands: (required) SVAML commands describing the call flow.
        :type commands: List[SvamlCommandDict]
        :param idempotency_key: (optional) Client-generated idempotency key to safely retry requests. If a request with the same key is received within 10 minutes, the cached response from the original request is returned. Using a random UUID (v4) is strongly recommended.
        :type idempotency_key: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        request_data = PatchCallBySessionAndNameRequest(
            session_id=session_id,
            call_name=call_name,
            commands=commands,
            **strip_unset(
                {
                    "idempotency_key": idempotency_key,
                }
            ),
            **kwargs,
        )
        return self._request(PatchCallBySessionAndNameEndpoint, request_data)
