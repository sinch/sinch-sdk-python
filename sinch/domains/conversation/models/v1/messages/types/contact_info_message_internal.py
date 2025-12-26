from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)
from sinch.domains.conversation.models.v1.messages.shared.name_info import (
    NameInfo,
)
from sinch.domains.conversation.models.v1.messages.shared.phone_number_info import (
    PhoneNumberInfo,
)
from sinch.domains.conversation.models.v1.messages.shared.address_info import (
    AddressInfo,
)
from sinch.domains.conversation.models.v1.messages.shared.email_info import (
    EmailInfo,
)
from sinch.domains.conversation.models.v1.messages.shared.organization_info import (
    OrganizationInfo,
)
from sinch.domains.conversation.models.v1.messages.shared.url_info import (
    UrlInfo,
)


class ContactInfoMessageInternal(BaseModelConfigurationResponse):
    name: NameInfo = Field(..., description="Name information of the contact.")
    phone_numbers: conlist(PhoneNumberInfo, min_length=1) = Field(
        description="Phone numbers of the contact (at least one required).",
    )
    addresses: Optional[conlist(AddressInfo)] = Field(
        default=None, description="Physical addresses of the contact."
    )
    email_addresses: Optional[conlist(EmailInfo)] = Field(
        default=None, description="Email addresses of the contact."
    )
    organization: Optional[OrganizationInfo] = Field(
        default=None, description="Organization info of the contact."
    )
    urls: Optional[conlist(UrlInfo)] = Field(
        default=None, description="URLs/websites associated with the contact."
    )
    birthday: Optional[str] = Field(
        default=None, description="Date of birth in YYYY-MM-DD format."
    )
