from typing import TypedDict

from typing_extensions import NotRequired


class TemplateVariableDict(TypedDict):
    key: NotRequired[str]
    preview_value: NotRequired[str]
