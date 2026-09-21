from typing import TypedDict

from typing_extensions import NotRequired

from sinch.domains.conversation.models.v1.apps.types.dispatch_retention_policy_type import (
    DispatchRetentionPolicyType,
)


class DispatchRetentionPolicyDict(TypedDict):
    retention_type: NotRequired[DispatchRetentionPolicyType]
    ttl_days: NotRequired[int]
