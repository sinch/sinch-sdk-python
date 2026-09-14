from typing import Union

from sinch.domains.voice.models.v2.types.phone_dict import PhoneDict
from sinch.domains.voice.models.v2.types.sip_from_dict import SipFromDict

CallOriginDict = Union[PhoneDict, SipFromDict]
