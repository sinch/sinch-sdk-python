import pytest

from sinch.domains.conversation.enums import (
    ConversationChannel,
    ConversationMetadataReportView,
    ConversationProcessingMode,
    ConversationRetentionPolicyType,
)


@pytest.mark.parametrize(
    "enum_cls, member_name",
    [
        (ConversationProcessingMode, "DISPATCH"),
        (ConversationMetadataReportView, "NONE"),
        (ConversationRetentionPolicyType, "MESSAGE_EXPIRE_POLICY"),
        (ConversationChannel, "WHATSAPP"),
    ],
)
def test_deprecated_enum_warns_on_lookup(enum_cls, member_name):
    with pytest.warns(DeprecationWarning, match="deprecated"):
        enum_cls(member_name)
