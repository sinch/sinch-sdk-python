from enum import Enum

from typing_extensions import deprecated


@deprecated(
    "ConversationProcessingMode is deprecated since 2.2.0 and unused; "
    "it will be removed in 3.0."
)
class ConversationProcessingMode(Enum):
    """
    .. deprecated:: 2.2.0
        Unused. Will be removed in 3.0.
    """

    DISPATCH = "DISPATCH"
    CONVERSATION = "CONVERSATION"


@deprecated(
    "ConversationMetadataReportView is deprecated since 2.2.0 and unused; "
    "it will be removed in 3.0."
)
class ConversationMetadataReportView(Enum):
    """
    .. deprecated:: 2.2.0
        Unused. Will be removed in 3.0.
    """

    NONE = "NONE"
    FULL = "FULL"


@deprecated(
    "ConversationRetentionPolicyType is deprecated since 2.2.0 and unused; "
    "it will be removed in 3.0."
)
class ConversationRetentionPolicyType(Enum):
    """
    .. deprecated:: 2.2.0
        Unused. Will be removed in 3.0.
    """

    MESSAGE_EXPIRE_POLICY = "MESSAGE_EXPIRE_POLICY"
    CONVERSATION_EXPIRE_POLICY = "CONVERSATION_EXPIRE_POLICY"
    PERSIST_RETENTION_POLICY = "PERSIST_RETENTION_POLICY"


@deprecated(
    "ConversationChannel is deprecated since 2.2.0 and unused;"
    "it will be removed in 3.0."
)
class ConversationChannel(Enum):
    """
    .. deprecated:: 2.2.0
        Unused. Will be removed in 3.0.
    """

    WHATSAPP = "WHATSAPP"
    RCS = "RCS"
    SMS = "SMS"
    MESSENGER = "MESSENGER"
    VIBER = "VIBER"
    VIBERBM = "VIBERBM"
    MMS = "MMS"
    INSTAGRAM = "INSTAGRAM"
    TELEGRAM = "TELEGRAM"
    KAKAOTALK = "KAKAOTALK"
    LINE = "LINE"
    WECHAT = "WECHAT"
