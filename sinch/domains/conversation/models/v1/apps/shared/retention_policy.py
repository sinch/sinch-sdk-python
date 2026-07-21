from typing import Optional
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.apps.types.retention_policy_type import (
    RetentionPolicyType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class RetentionPolicy(BaseModelConfiguration):
    retention_type: Optional[RetentionPolicyType] = None
    ttl_days: Optional[StrictInt] = Field(
        default=None,
        description="Optional. The days before a message or conversation is eligible for deletion. Default value is 180. The ttl_days value has no effect when retention_type is `PERSIST_RETENTION_POLICY`. The valid values for this field are [1 - 3650]. Note that retention cleanup job runs once every twenty-four hours which can lead to delay i.e., messages and conversations are not deleted on the minute they become eligible for deletion.",
    )
