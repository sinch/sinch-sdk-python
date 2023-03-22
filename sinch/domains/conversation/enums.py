from enum import Enum


class ConversationProcessingMode(Enum):
    DISPATCH = "DISPATCH"
    CONVERSATION = "CONVERSATION"


class ConversationMetadataReportView(Enum):
    NONE = "NONE"
    FULL = "FULL"


class ConversationRetentionPolicyType(Enum):
    MESSAGE_EXPIRE_POLICY = "MESSAGE_EXPIRE_POLICY"
    CONVERSATION_EXPIRE_POLICY = "CONVERSATION_EXPIRE_POLICY"
    PERSIST_RETENTION_POLICY = "PERSIST_RETENTION_POLICY"


class ConversationChannel(Enum):
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
