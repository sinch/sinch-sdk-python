from typing import Literal, Optional

from sinch.core.models.internal.utils import strip_unset
from sinch.core.pagination import LinkBasedPaginator, Paginator
from sinch.core.sentinel import UNSET, UnsetOr
from sinch.domains.voice.api.v2.base.base_voice import BaseVoice
from sinch.domains.voice.api.v2.internal.services_endpoints import (
    CreateServiceEndpoint,
    DeleteServiceEndpoint,
    GetServiceEndpoint,
    ListServicesEndpoint,
    UpdateServiceEndpoint,
)
from sinch.domains.voice.models.v2.services.internal.list_services_response import (
    ListServicesResponse,
)
from sinch.domains.voice.models.v2.services.internal.request.create_service_request import (
    CreateServiceRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.list_services_request import (
    ListServicesRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.service_id_request import (
    ServiceIdRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.update_service_request import (
    UpdateServiceRequest,
)
from sinch.domains.voice.models.v2.services.response.service_response import (
    ServiceResponse,
)
from sinch.domains.voice.models.v2.services.response.service_short_response import (
    ServiceShortResponse,
)
from sinch.domains.voice.models.v2.services.types.call_behavior_dict import (
    CallBehaviorDict,
)


class Services(BaseVoice):
    def list(
        self,
        filter: Optional[str] = None,
        is_default: Optional[bool] = None,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        **kwargs,
    ) -> Paginator[ListServicesResponse, ServiceShortResponse]:
        """
        List and filter the services configured for a project.

        :param filter: (optional) Filter services by name or description. Returns all services where either the name or description contains the specified value (case-insensitive partial match).
        :type filter: Optional[str]
        :param is_default: (optional) Return only the default service.
        :type is_default: Optional[bool]
        :param page_size: (optional) Number of items to be returned on each page.
        :type page_size: Optional[int]
        :param page: (optional) Page number (1-based).
        :type page: Optional[int]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: LinkBasedPaginator with ServiceShortResponse items
        :rtype: Paginator[ListServicesResponse,ServiceShortResponse]

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        return LinkBasedPaginator._initialize(
            sinch=self._sinch,
            endpoint=ListServicesEndpoint(
                project_id=self._sinch.configuration.project_id,
                request_data=ListServicesRequest(
                    filter=filter,
                    is_default=is_default,
                    page_size=page_size,
                    page=page,
                    **kwargs,
                ),
            ),
        )

    def create(
        self,
        name: str,
        description: UnsetOr[Optional[str]] = UNSET,
        is_default: UnsetOr[Optional[bool]] = UNSET,
        call_behavior: UnsetOr[Optional[CallBehaviorDict]] = UNSET,
        idempotency_key: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> ServiceResponse:
        """
        Creates a new voice service.

        :param name: (required) The name of the service. Must be 1-64 characters, with no leading, trailing, or repeated whitespace. Regex pattern: `^\\S+(\\s+\\S+)*$`.
        :type name: str
        :param description: (optional) A description of the service. Must be at most 255 characters, with no leading, trailing, or repeated whitespace. Regex pattern: `^\\S+(\\s+\\S+)*$`.
        :type description: UnsetOr[Optional[str]]
        :param is_default: (optional) Whether this service is the project default. The default service is used when no specific service is specified in API requests
        :type is_default: UnsetOr[Optional[bool]]
        :param call_behavior: (optional) Defines how calls are handled for this service.
        :type call_behavior: UnsetOr[Optional[CallBehaviorDict]]
        :param idempotency_key: (optional) Client-generated idempotency key to safely retry requests. If a request with the same key is received within 10 minutes, the cached response from the original request is returned. Using a random UUID (v4) is strongly recommended.
        :type idempotency_key: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The created service.
        :rtype: ServiceResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        request_data = CreateServiceRequest(
            name=name,
            **strip_unset(
                {
                    "description": description,
                    "is_default": is_default,
                    "call_behavior": call_behavior,
                    "idempotency_key": idempotency_key,
                }
            ),
            **kwargs,
        )
        return self._request(CreateServiceEndpoint, request_data)

    def get(self, service_id: str, **kwargs) -> ServiceResponse:
        """
        Retrieve detailed information about a specific service using its unique identifier.

        :param service_id: (required) The ID of the service.
        :type service_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The service details.
        :rtype: ServiceResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        request_data = ServiceIdRequest(service_id=service_id, **kwargs)
        return self._request(GetServiceEndpoint, request_data)

    def update(
        self,
        service_id: str,
        name: UnsetOr[Optional[str]] = UNSET,
        description: UnsetOr[Optional[str]] = UNSET,
        is_default: UnsetOr[Optional[Literal[True]]] = UNSET,
        call_behavior: UnsetOr[Optional[CallBehaviorDict]] = UNSET,
        idempotency_key: UnsetOr[Optional[str]] = UNSET,
        **kwargs,
    ) -> ServiceResponse:
        """
        Updates an existing service resource with the provided properties. Only the fields included in the request body will be modified; omitted fields remain unchanged.

        To set a service as the default for the project, include `is_default=True`.
        Note that each project can have only one default service. Setting a new default will automatically remove the default status from the previously designated service.

        :param service_id: (required) The ID of the service.
        :type service_id: str
        :param name: (optional) The name of the service. Must be 1-64 characters, with no leading, trailing, or repeated whitespace. Regex pattern: `^\\S+(\\s+\\S+)*$`.
        :type name: str
        :param description: (optional) A description of the service. Must be at most 255 characters, with no leading, trailing, or repeated whitespace. Regex pattern: `^\\S+(\\s+\\S+)*$`.
        :type description: UnsetOr[Optional[str]]
        :param is_default: (optional) Whether this service is the project default. Setting this to `false` is invalid.
        :type is_default: UnsetOr[Optional[Literal[True]]]
        :param call_behavior: (optional) Defines how calls are handled for this service.
        :type call_behavior: UnsetOr[Optional[CallBehaviorDict]]
        :param idempotency_key: (optional) Client-generated idempotency key to safely retry requests. If a request with the same key is received within 10 minutes, the cached response from the original request is returned. Using a random UUID (v4) is strongly recommended.
        :type idempotency_key: UnsetOr[Optional[str]]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: The updated service.
        :rtype: ServiceResponse

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        request_data = UpdateServiceRequest(
            service_id=service_id,
            **strip_unset(
                {
                    "name": name,
                    "description": description,
                    "is_default": is_default,
                    "call_behavior": call_behavior,
                    "idempotency_key": idempotency_key,
                }
            ),
            **kwargs,
        )
        return self._request(UpdateServiceEndpoint, request_data)

    def delete(self, service_id: str, **kwargs) -> None:
        """
        Deletes a service permanently.

        **Important:** The default service cannot be deleted. To delete the current default service,
        a different service must first be designated as the default using the PATCH endpoint.

        :param service_id: (required) The ID of the service.
        :type service_id: str
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict
        :returns: None
        :rtype: None

        For detailed documentation, visit https://developers.sinch.com/docs/voice-2.0.
        """
        request_data = ServiceIdRequest(service_id=service_id, **kwargs)
        return self._request(DeleteServiceEndpoint, request_data)
