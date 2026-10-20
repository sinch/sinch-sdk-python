from typing import TypedDict

from typing_extensions import NotRequired


class ContactSettingsDict(TypedDict):
    unified_contact_id_enabled: NotRequired[bool]
