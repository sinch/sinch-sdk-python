from sinch.domains.numbers.api.v1.base import BaseNumbers
from sinch.domains.numbers.api.v1.internal import (
    GetCallbackConfigurationEndpoint, UpdateCallbackConfigurationEndpoint
)
from sinch.domains.numbers.models.v1.internal import UpdateCallbackConfigurationRequest
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest
from sinch.domains.numbers.models.v1.response import CallbackConfigurationResponse


class CallbackConfiguration(BaseNumbers):

    def get(
        self,
        **kwargs
    ) -> CallbackConfigurationResponse:
        """
        Returns the callback configuration for the specified project

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: The callback configuration for the project.
        :rtype: NumbersCallbackConfigResponse

        For detailed documentation, visit: https://developers.sinch.com
        """
        request_data = None
        if kwargs:
            request_data = BaseModelConfigurationRequest(**kwargs)
        return self._request(GetCallbackConfigurationEndpoint, request_data)

    def update(
        self,
        hmac_secret: str,
        **kwargs
    ) -> CallbackConfigurationResponse:
        """
        Updates the callback configuration for the specified project

        :param hmac_secret: The HMAC secret used to sign the callback requests.
        :type hmac_secret: str

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: The updated callback configuration for the project.
        :rtype: NumbersCallbackConfigResponse

        For detailed documentation, visit https://developers.sinch.com
        """
        request_data = UpdateCallbackConfigurationRequest(
            hmac_secret=hmac_secret,
            **kwargs
        )
        return self._request(UpdateCallbackConfigurationEndpoint, request_data)
