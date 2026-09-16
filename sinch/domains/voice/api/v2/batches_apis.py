from typing import Dict, List, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.api.v2.base.base_voice import BaseVoice
from sinch.domains.voice.api.v2.internal.batches_endpoints import (
    GetBatchCallSummaryEndpoint,
    GetBatchDetailsEndpoint,
    StartBatchEndpoint,
    StopBatchProcessingEndpoint,
)
from sinch.domains.voice.models.v2.batches.internal.request.batch_id_request import (
    BatchIdRequest,
)
from sinch.domains.voice.models.v2.batches.internal.request.start_batch_request import (
    StartBatchRequest,
)
from sinch.domains.voice.models.v2.batches.response.batch_details_response import (
    BatchDetailsResponse,
)
from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)
from sinch.domains.voice.models.v2.batches.response.start_batch_response import (
    StartBatchResponse,
)
from sinch.domains.voice.models.v2.batches.types.batch_options_dict import (
    BatchOptionsDict,
)
from sinch.domains.voice.models.v2.svaml.types.svaml_command_dict import (
    SvamlCommandDict,
)


class Batches(BaseVoice):
    def start(
        self,
        commands: List[SvamlCommandDict],
        parameters: List[Dict[str, str]],
        service_id: Optional[str] = None,
        batch_options: UnsetOr[Optional[BatchOptionsDict]] = UNSET,
        idempotency_key: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> StartBatchResponse:
        """
        Create a batch of outbound calls, associated to the project's default service or to the service specified in the `serviceId` query parameter.

        :param commands: (required) SVAML commands describing the call flow.
        :type commands: List[SvamlCommandDict]
        :param parameters: (required) Parameter sets for dynamic placeholders in the commands. One entry queues one call.
        :type parameters: List[Dict[str, str]]
        :param service_id: (optional) The ID of the service to use for the call. If omitted, the project's default service is used.
        :type service_id: Optional[str]
        :param batch_options: (optional) Options controlling how the batch is processed (maximum calls per second, time-to-live).
        :type batch_options: UnsetOr[Optional[BatchOptionsDict]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The queued batch of call sessions.
        :rtype: StartBatchResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice/.
        """
        request_data = StartBatchRequest(
            commands=commands,
            parameters=parameters,
            service_id=service_id,
            **strip_unset(
                {
                    "batch_options": batch_options,
                    "idempotency_key": idempotency_key,
                }
            ),
            **kwargs,
        )
        return self._request(StartBatchEndpoint, request_data)

    def get(self, batch_id: str, **kwargs) -> BatchSummaryResponse:
        """
        Retrieve a summary of a batch call operation, including statistics on completed, failed, in-progress, and queued calls. This provides an overview of the batch execution state and individual call session states.

        :param batch_id: (required) The ID of the batch.
        :type batch_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The batch call summary.
        :rtype: BatchSummaryResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice/.
        """
        request_data = BatchIdRequest(batch_id=batch_id, **kwargs)
        return self._request(GetBatchCallSummaryEndpoint, request_data)

    def get_details(self, batch_id: str, **kwargs) -> BatchDetailsResponse:
        """
        Retrieve per-session details for a batch call operation, including the current state of each call session in the batch.

        Use this endpoint when individual session-level visibility is needed (for example, to inspect which sessions are `QUEUED`, `IN_PROGRESS` or `COMPLETED`). `EXPIRED` sessions are never returned because they were never initiated.

        :param batch_id: (required) The ID of the batch.
        :type batch_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The per-session batch details.
        :rtype: BatchDetailsResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice/.
        """
        request_data = BatchIdRequest(batch_id=batch_id, **kwargs)
        return self._request(GetBatchDetailsEndpoint, request_data)

    def stop(self, batch_id: str, **kwargs) -> None:
        """
        Stop processing a batch of call sessions. This will prevent any queued calls in the batch from being initiated. Calls that are already in progress will not be affected and will continue until completion.

        :param batch_id: (required) The ID of the batch.
        :type batch_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/voice/.
        """
        request_data = BatchIdRequest(batch_id=batch_id, **kwargs)
        return self._request(StopBatchProcessingEndpoint, request_data)
