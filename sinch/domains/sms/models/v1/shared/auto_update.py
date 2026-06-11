from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class AddKeyword(BaseModelConfigurationResponse):
    first_word: StrictStr = Field(
        default=...,
        description="Opt-in keyword like 'JOIN' if auto_update.to is a dedicated long/short number, "
        "or unique brand keyword like 'Sinch' if it is a shared short code.",
    )
    second_word: Optional[StrictStr] = Field(
        default=None,
        description="Opt-in keyword like 'JOIN' if auto_update.to is a shared short code.",
    )


class RemoveKeyword(BaseModelConfigurationResponse):
    first_word: StrictStr = Field(
        default=...,
        description="Opt-out keyword like 'LEAVE' if auto_update.to is a dedicated long/short number, "
        "or unique brand keyword like 'Sinch' if it is a shared short code.",
    )
    second_word: Optional[StrictStr] = Field(
        default=None,
        description="Opt-out keyword like 'LEAVE' if auto_update.to is a shared short code.",
    )


class AutoUpdate(BaseModelConfigurationResponse):
    to: StrictStr = Field(
        default=...,
        description="Short code or long number addressed in MO. "
        "Must be a valid phone number or short code provisioned by your account manager.",
    )
    add: Optional[AddKeyword] = Field(
        default=None,
        description="Keyword to be sent in MO to add MSISDN to the group.",
    )
    remove: Optional[RemoveKeyword] = Field(
        default=None,
        description="Keyword to be sent in MO to remove MSISDN from the group.",
    )
