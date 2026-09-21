from typing import Optional
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.apps.types.dispatch_retention_policy_type import (
    DispatchRetentionPolicyType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class DispatchRetentionPolicy(BaseModelConfiguration):
    retention_type: Optional[DispatchRetentionPolicyType] = None
    ttl_days: Optional[StrictInt] = Field(
        default=None,
        description="Optional. The days before a message is eligible for deletion. The valid range is `[0 - 7]`. In the case of a `0` day TTL, messages aren't stored at all. Note the retention cleanup job runs once every twenty-four hours, so messages are not deleted on the minute they become eligible for deletion.",
    )
