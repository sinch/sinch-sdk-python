from sinch.domains.numbers.api.v1.base import BaseNumbers
from sinch.domains.numbers.api.v1.internal import (
    GetNumbersCallbacksConfigEndpoint, UpdateNumbersCallbacksConfigEndpoint
)
from sinch.domains.numbers.models.v1.internal import UpdateNumbersCallbacksConfigRequest
from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigRequest
from sinch.domains.numbers.models.v1.response import NumbersCallbackConfigResponse


class Callbacks(BaseNumbers):

    def get_configuration(
        self,
        **kwargs
    ) -> NumbersCallbackConfigResponse:
        """
        Returns the callbacks configuration for the specified project

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: The callbacks configuration for the project.
        :rtype: NumbersCallbackConfigResponse

        For detailed documentation, visit: https://developers.sinch.com
        """
        request_data = None
        if kwargs:
            request_data = BaseModelConfigRequest(**kwargs)
        return self._request(GetNumbersCallbacksConfigEndpoint, request_data)

    def update_configuration(
        self,
        hmac_secret,
        **kwargs
    ) -> NumbersCallbackConfigResponse:
        """
        Updates the callbacks configuration for the specified project

        :param hmac_secret: The HMAC secret used to sign the callback requests.
        :type hmac_secret: str

        :param kwargs: Additional parameters for the request.
        :type kwargs: dict

        :returns: The updated callbacks configuration for the project.
        :rtype: NumbersCallbackConfigResponse

        For detailed documentation, visit https://developers.sinch.com
        """
        request_data = UpdateNumbersCallbacksConfigRequest(
            hmac_secret=hmac_secret,
            **kwargs
        )
        return self._request(UpdateNumbersCallbacksConfigEndpoint, request_data)
