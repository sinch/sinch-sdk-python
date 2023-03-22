from dataclasses import dataclass
from typing import List
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.conversation.models import (
    SinchConversationApp
)


@dataclass
class CreateConversationAppResponse(SinchConversationApp):
    pass


@dataclass
class DeleteConversationAppResponse(SinchBaseModel):
    pass


@dataclass
class ListConversationAppsResponse(SinchBaseModel):
    apps: List[SinchConversationApp]


@dataclass
class GetConversationAppResponse(SinchConversationApp):
    pass


@dataclass
class UpdateConversationAppResponse(SinchConversationApp):
    pass
