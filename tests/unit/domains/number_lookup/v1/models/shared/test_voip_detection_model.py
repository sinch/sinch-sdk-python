from sinch.domains.number_lookup.models.v1.shared import VoIPDetection


def test_voip_detection_valid_expects_parsed_data():
    """Test a valid instance of VoIPDetection"""
    data = {"probability": "High"}
    voip_detection = VoIPDetection(**data)

    assert voip_detection.probability == "High"


def test_voip_detection_optional_fields_expects_parsed_data():
    """Test missing optional fields in VoIPDetection"""
    data = {}
    voip_detection = VoIPDetection(**data)

    assert voip_detection.probability is None
