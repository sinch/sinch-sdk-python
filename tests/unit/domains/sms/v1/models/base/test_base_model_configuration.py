from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


def test_model_dump_for_query_params_expects_simple_fields():
    """
    Test that simple fields are returned as-is.
    """

    class TestModel(BaseModelConfigurationRequest):
        batch_id: str
        status: str = None

    model = TestModel(
        batch_id="01FC66621XXXXX119Z8PMV1QPQ", status="delivered"
    )
    result = model.model_dump_for_query_params()

    assert result["batch_id"] == "01FC66621XXXXX119Z8PMV1QPQ"
    assert result["status"] == "delivered"


def test_model_dump_for_query_params_expects_list_to_comma_separated_string():
    """
    Test that lists are converted to comma-separated strings.
    """

    class TestModel(BaseModelConfigurationRequest):
        status: list[str] = None
        code: list[int] = None

    model = TestModel(status=["Delivered", "Failed"], code=[15, 0])
    result = model.model_dump_for_query_params()

    assert result["status"] == "Delivered,Failed"
    assert result["code"] == "15,0"
