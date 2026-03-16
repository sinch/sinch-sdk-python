from sinch.domains.numbers.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


# Base for NumberSinchEvent used for request modeling.
# Not to be confused with a response as in BaseModelConfigurationResponse.
class WebhookEvent(BaseModelConfigurationResponse):
    pass
