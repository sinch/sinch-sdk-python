from typing import Dict, Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.voice.models.v2.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.voice.models.v2.types.session_state import SessionState


class BatchSessionSummary(BaseModelConfiguration):
    id: Optional[StrictStr] = Field(
        default=None,
        description="Unique identifier of the call session within the batch. This identifies the session, not an individual call. Use it with `/v2/projects/{projectId}/sessions/{sessionId}` to retrieve full session details.",
    )
    state: Optional[SessionState] = Field(default=None)
    parameters: Optional[Dict[StrictStr, StrictStr]] = Field(
        default=None,
        description="Plain key-value set of parameters from the batch request `parameters` entry that was used to initiate this call session.",
    )


class BatchDetailsResponse(BaseModelConfiguration):
    sessions: conlist(BatchSessionSummary) = Field(default=...)
