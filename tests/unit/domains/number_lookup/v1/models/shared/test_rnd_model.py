from sinch.domains.number_lookup.models.v1.shared import Rnd


def test_rnd_valid_expects_parsed_data():
    """Test a valid instance of Rnd"""
    data = {"disconnected": True}
    rnd = Rnd(**data)

    assert rnd.disconnected is True


def test_rnd_optional_fields_expects_parsed_data():
    """Test missing optional fields in Rnd"""
    data = {}
    rnd = Rnd(**data)

    assert rnd.disconnected is None
