from typing import TypedDict

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.apps.types.retention_policy_type import (
    RetentionPolicyType,
)


class RetentionPolicyDict(TypedDict):
    retention_type: NotRequired[RetentionPolicyType]
    ttl_days: NotRequired[int]
