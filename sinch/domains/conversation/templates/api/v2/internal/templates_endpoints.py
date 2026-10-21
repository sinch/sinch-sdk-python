from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.templates.api.v2.internal.base.templates_endpoint import (
    TemplatesEndpoint,
)
from sinch.domains.conversation.templates.models.v2.internal.create_template_request import (
    CreateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_templates_request import (
    ListTemplatesRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_templates_response import (
    ListTemplatesResponse,
)
from sinch.domains.conversation.templates.models.v2.internal.list_translations_request import (
    ListTranslationsRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.list_translations_response import (
    ListTranslationsResponse,
)
from sinch.domains.conversation.templates.models.v2.internal.template_id_request import (
    TemplateIdRequest,
)
from sinch.domains.conversation.templates.models.v2.internal.update_template_request import (
    UpdateTemplateRequest,
)
from sinch.domains.conversation.templates.models.v2.response.template_response import (
    TemplateResponse,
)


class ListTemplatesEndpoint(TemplatesEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/templates"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ListTemplatesRequest,
        response_model=ListTemplatesResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class CreateTemplateEndpoint(TemplatesEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/templates"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: CreateTemplateRequest,
        response_model=TemplateResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ListTranslationsEndpoint(TemplatesEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/templates/{template_id}/translations"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"language_code", "translation_version"}

    def __init__(
        self,
        project_id: str,
        request_data: ListTranslationsRequest,
        response_model=ListTranslationsResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class UpdateTemplateEndpoint(TemplatesEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/templates/{template_id}"
    HTTP_METHOD = HTTPMethods.PUT.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: UpdateTemplateRequest,
        response_model=TemplateResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetTemplateEndpoint(TemplatesEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/templates/{template_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: TemplateIdRequest,
        response_model=TemplateResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeleteTemplateEndpoint(TemplatesEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/templates/{template_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: TemplateIdRequest):
        super().__init__(project_id, request_data)
