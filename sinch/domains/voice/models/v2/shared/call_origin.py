from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from sinch.domains.voice.models.v2.shared.phone import Phone
from sinch.domains.voice.models.v2.shared.sip_from import SipFrom

CallOrigin = Annotated[Union[Phone, SipFrom], Field(discriminator="type")]
