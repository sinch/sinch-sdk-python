from datetime import datetime, timezone

from sinch.domains.voice.models.v2.services.internal.list_services_response import (
    ListServicesResponse,
)
from sinch.domains.voice.models.v2.services.response.service_short_response import (
    ServiceShortResponse,
)


def test_list_services_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListServicesResponse(
        services=[
            {
                "service_id": "6e124178-c29d-46a5-943c-5c2ae544aade",
                "project_id": "5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
                "create_time": "2025-01-01T00:00:00Z",
                "update_time": "2025-01-02T00:00:00Z",
                "name": "Primary Service",
                "description": "The primary service for the project.",
                "is_default": True,
            }
        ],
        links={
            "first": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20",
            "last": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20",
            "self": "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20",
        },
        meta={"total_count": 1, "page_count": 1},
    )

    assert len(model.services) == 1
    service = model.services[0]
    assert isinstance(service, ServiceShortResponse)
    assert service.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert service.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert service.create_time == datetime(
        2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc
    )
    assert service.update_time == datetime(
        2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc
    )
    assert service.name == "Primary Service"
    assert service.description == "The primary service for the project."
    assert service.is_default is True

    assert model.links.first == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20"
    )
    assert model.links.last == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20"
    )
    assert model.links.self_ == (
        "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20"
    )
    assert model.links.next is None
    assert model.links.prev is None

    assert model.meta.total_count == 1
    assert model.meta.page_count == 1
    assert model.content == model.services

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert len(alias_dump["services"]) == 1
    service_dump = alias_dump["services"][0]
    assert service_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert service_dump["projectId"] == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert service_dump["createTime"] == "2025-01-01T00:00:00Z"
    assert service_dump["updateTime"] == "2025-01-02T00:00:00Z"
    assert service_dump["name"] == "Primary Service"
    assert service_dump["description"] == "The primary service for the project."
    assert service_dump["isDefault"] is True
    assert alias_dump["links"] == {
        "first": (
            "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20"
        ),
        "last": (
            "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20"
        ),
        "self": (
            "https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/services?page=1&pageSize=20"
        ),
    }
    assert alias_dump["meta"] == {"totalCount": 1, "pageCount": 1}
