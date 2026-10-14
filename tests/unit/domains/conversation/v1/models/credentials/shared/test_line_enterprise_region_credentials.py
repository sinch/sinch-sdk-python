import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_japan import (
    LineEnterpriseCredentialsJapan,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_thailand import (
    LineEnterpriseCredentialsThailand,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_region_credentials import (
    LineEnterpriseRegionCredentials,
)

adapter = TypeAdapter(LineEnterpriseRegionCredentials)

CREDENTIALS = {"token": "t", "secret": "s"}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({"line_japan": CREDENTIALS}, LineEnterpriseCredentialsJapan),
        ({"line_thailand": CREDENTIALS}, LineEnterpriseCredentialsThailand),
    ],
    ids=["japan", "thailand"],
)
def test_line_enterprise_region_credentials_resolves_each_variant(
    payload, expected_type
):
    """
    Expects each region to resolve from the region key it declares.
    """
    with response_parsing_scope():
        credentials = adapter.validate_python(payload)

    assert type(credentials) is expected_type


def test_line_enterprise_region_credentials_resolves_to_unknown_in_a_response():
    """
    Expects a region added to the API later to be parsed as SinchRawResponse
    keeping the payload.
    """
    payload = {"line_korea": CREDENTIALS}

    with response_parsing_scope():
        credentials = adapter.validate_python(payload)

    assert isinstance(credentials, SinchRawResponse)
    assert credentials.model_dump() == payload


def test_line_enterprise_region_credentials_rejects_an_unknown_region_in_a_request():
    """
    Expects a region the SDK does not know to be rejected when configuring an
    app.
    """
    with pytest.raises(ValidationError):
        adapter.validate_python({"line_korea": CREDENTIALS})
