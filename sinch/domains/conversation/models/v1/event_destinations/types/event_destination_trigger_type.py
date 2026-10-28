from typing import Literal, Union

from pydantic import StrictStr


EventDestinationTriggerType = Union[
    Literal[
        "UNSPECIFIED_TRIGGER",
        "MESSAGE_DELIVERY",
        "EVENT_DELIVERY",
        "MESSAGE_INBOUND",
        "EVENT_INBOUND",
        "CONVERSATION_START",
        "CONVERSATION_STOP",
        "CONTACT_CREATE",
        "CONTACT_DELETE",
        "CONTACT_MERGE",
        "CONTACT_UPDATE",
        "UNSUPPORTED",
        "OPT_IN",
        "OPT_OUT",
        "CAPABILITY",
        "CONVERSATION_DELETE",
        "CONTACT_IDENTITIES_DUPLICATION",
        "CHANNEL_EVENT",
        "SMART_CONVERSATION",
        "MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION",
        "RECORD_NOTIFICATION",
        "MESSAGE_SUBMIT",
    ],
    StrictStr,
]
