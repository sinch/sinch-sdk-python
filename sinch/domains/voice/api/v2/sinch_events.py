from typing import Any, Dict, List, Optional, Union

from sinch.core.internal.sinch_events.authorization_helpers import (
    validate_authentication_header,
)
from sinch.core.internal.sinch_events.utils import (
    decode_payload,
    parse_json,
)
from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.models.v2.sinch_events.incoming_call_events_dict import (
    IncomingCallEventsDict,
)
from sinch.domains.voice.models.v2.sinch_events.voice_sinch_event_request import (
    VoiceSinchEventRequest,
)
from sinch.domains.voice.models.v2.sinch_events.voice_sinch_event_response import (
    VoiceSinchEventResponse,
)
from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
    SvamlCommandDict,
)


class SinchEvents:
    """
    Handler for Voice API v2 Sinch Events.
    """

    def validate_authentication_header(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        body: Union[str, bytes],
        service_id: str,
        service_secret: str,
    ) -> bool:
        """
        Validate the Authorization header of an incoming Sinch Event request.

        :param method: (required) HTTP method of the incoming request.
        :type method: str
        :param path: (required) Canonicalized resource path of the incoming request.
        :type path: str
        :param headers: (required) Incoming request's headers.
        :type headers: Dict[str, str]
        :param body: (required) Incoming request's raw body.
        :type body: Union[str, bytes]
        :param service_secret: (required) The service secret used to validate the authentication header.
        :type service_secret: str
        :param service_id: (required) The service key used to validate the authentication header.
        :type service_id: str
        :returns: True if the Authorization header is valid.
        :rtype: bool
        :raises ValueError: If no service secret is available.
        """

        return validate_authentication_header(
            key=service_id,
            secret=service_secret,
            headers=headers,
            body=body,
            path=path,
            method=method,
        )

    def parse_event(
        self,
        event_body: Union[str, bytes, Dict[str, Any]],
        headers: Optional[Dict[str, str]] = None,
    ) -> VoiceSinchEventRequest:
        """
        Parse an incoming sinch event request body into a typed event.

        :param event_body: The event payload (JSON string, raw bytes, or dict).
        :type event_body: Union[str, bytes, Dict[str, Any]]
        :param headers: Request headers (used to decode charset when event_body is bytes).
        :type headers: Optional[Dict[str, str]]
        :returns: The parsed sinch event request.
        :rtype: VoiceSinchEventRequest
        :raises ValueError: If JSON parsing fails or the payload is invalid.
        """
        if isinstance(event_body, bytes):
            event_body = parse_json(decode_payload(event_body, headers))
        elif isinstance(event_body, str):
            event_body = parse_json(event_body)

        return VoiceSinchEventRequest(**event_body)

    def build_response(
        self,
        commands: List[SvamlCommandDict],
    ) -> VoiceSinchEventResponse:
        """
        Build the SVAML response to return from a sinch event handler.

        :param commands: (required) The ordered list of SVAML commands to execute.
        :type commands: List[SvamlCommandDict]
        :returns: The sinch event response, ready to be serialized.
        :rtype: VoiceSinchEventResponse
        """
        return VoiceSinchEventResponse(commands=commands)

    def build_incoming_call_response(
        self,
        commands: List[SvamlCommandDict],
        call_name: UnsetOr[Optional[str]] = UNSET,
        events: UnsetOr[Optional[IncomingCallEventsDict]] = UNSET,
    ) -> VoiceSinchEventResponse:
        """
        Build the SVAML response to return from the handler for a `call.incoming` sinch event.

        :param commands: (required) The ordered list of SVAML commands to execute.
        :type commands: List[SvamlCommandDict]
        :param call_name: (optional) Name of the call.
        :type call_name: UnsetOr[Optional[str]]
        :param events: (optional) Commands to execute on specific events for this call.
        :type events: UnsetOr[Optional[IncomingCallEventsDict]]
        :returns: The sinch event response, ready to be serialized.
        :rtype: VoiceSinchEventResponse
        """
        return VoiceSinchEventResponse(
            commands=commands,
            **strip_unset({"call_name": call_name, "events": events}),
        )

    def serialize_response(self, response: VoiceSinchEventResponse) -> Dict[str, Any]:
        """
        Serialize a sinch event response into a JSON-ready dict.

        :param response: The sinch event response to serialize.
        :type response: VoiceSinchEventResponse
        :returns: The response body to return from the sinch event handler.
        :rtype: Dict[str, Any]
        """
        return response.model_dump(mode="json", by_alias=True, exclude_unset=True)
