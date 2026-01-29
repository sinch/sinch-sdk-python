from typing import Dict, TypedDict
from typing_extensions import NotRequired


class TemplateReferenceChannelSpecificDict(TypedDict):
    template_id: str
    version: NotRequired[str]
    language_code: NotRequired[str]
    parameters: NotRequired[Dict[str, str]]


class TemplateReferenceOmniChannelDict(TemplateReferenceChannelSpecificDict):
    version: str


class TemplateMessageDict(TypedDict):
    channel_template: NotRequired[
        Dict[str, TemplateReferenceChannelSpecificDict]
    ]
    omni_template: NotRequired[TemplateReferenceOmniChannelDict]
