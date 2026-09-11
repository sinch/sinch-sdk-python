from typing import Dict, List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.api.v2.base.base_voice import BaseVoice
from sinch.domains.voice.api.v2.internal.calls_endpoints import (
    StartCallEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)
from sinch.domains.voice.models.v2.calls.types.batch_options_dict import (
    BatchOptionsDict,
)
from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
    SvamlCommandDict,
)


class Calls(BaseVoice):
    def start(
        self,
        commands: List[SvamlCommandDict],
        service_id: Optional[str] = None,
        parameters: UnsetOr[Optional[List[Dict[str, str]]]] = UNSET,
        batch_options: UnsetOr[Optional[BatchOptionsDict]] = UNSET,
        idempotency_key: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> StartCallResponse:
        """
        Create a new outbound call, or a batch of outbound calls, associated to the project's default service or to the service specified in the `serviceId` query parameter.

        If ``parameters`` is provided a batch of call sessions is initiated, one per entry; ``batch_options`` is only valid in that mode.

        :param commands: (required) SVAML commands describing the call flow.
        :type commands: List[SvamlCommandDict]
        :param service_id: (optional) The ID of the service to use for the call. If omitted, the project's default service is used.
        :type service_id: Optional[str]
        :param parameters: (optional) Parameter sets for dynamic placeholders in the commands. One entry queues one call.
        :type parameters: UnsetOr[Optional[List[Dict[str, str]]]]
        :param batch_options: (optional) Options controlling how the batch is processed (maximum calls per second, time-to-live). Only valid when ``parameters`` is provided.
        :type batch_options: UnsetOr[Optional[BatchOptionsDict]]
        :param idempotency_key: (optional) Client-generated idempotency key to safely retry requests. If a request with the same key is received within 10 minutes, the cached response from the original request is returned. Using a random UUID (v4) is strongly recommended.
        :type idempotency_key: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The created call session, or the queued batch of call sessions.
        :rtype: StartCallResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice/.
        """
        request_data = StartCallRequest(
            commands=commands,
            service_id=service_id,
            **strip_unset(
                {
                    "parameters": parameters,
                    "batch_options": batch_options,
                    "idempotency_key": idempotency_key,
                }
            ),
            **kwargs,
        )
        return self._request(StartCallEndpoint, request_data)
