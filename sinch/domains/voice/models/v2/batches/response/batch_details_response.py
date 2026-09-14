from typing import Optional

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


class BatchDetailsResponse(BaseModelConfiguration):
    sessions: conlist(BatchSessionSummary) = Field(default=...)
