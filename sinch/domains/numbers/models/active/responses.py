from dataclasses import dataclass
from sinch.domains.numbers.models.active import ActiveNumber


@dataclass
class UpdateNumberConfigurationResponse(ActiveNumber):
    pass


@dataclass
class GetNumberConfigurationResponse(ActiveNumber):
    pass


@dataclass
class ReleaseNumberFromProjectResponse(ActiveNumber):
    pass
