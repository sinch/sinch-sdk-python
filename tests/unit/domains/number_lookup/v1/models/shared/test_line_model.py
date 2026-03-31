from datetime import datetime, timezone
from sinch.domains.number_lookup.models.v1.shared import Line


def test_line_valid_expects_parsed_data():
    """Test a valid instance of Line"""
    data = {
        "carrier": "T-Mobile USA",
        "type": "Mobile",
        "mobileCountryCode": "310",
        "mobileNetworkCode": "260",
        "ported": True,
        "portingDate": "2024-06-15T14:30:00+00:00",
    }
    line = Line(**data)

    assert line.carrier == "T-Mobile USA"
    assert line.type == "Mobile"
    assert line.mobile_country_code == "310"
    assert line.mobile_network_code == "260"
    assert line.ported is True
    expected_porting_date = datetime(
        2024, 6, 15, 14, 30, 0, tzinfo=timezone.utc
    )
    assert line.porting_date == expected_porting_date


def test_line_optional_fields_expects_parsed_data():
    """Test missing optional fields in Line"""
    data = {}
    line = Line(**data)

    assert line.carrier is None
    assert line.type is None
    assert line.mobile_country_code is None
    assert line.mobile_network_code is None
    assert line.ported is None
    assert line.porting_date is None
