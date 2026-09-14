from sinch.domains.voice.models.v2.shared.phone import Phone, PhoneDetails


def test_phone_details_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = PhoneDetails(number="+4673522488")

    assert model.number == "+4673522488"


def test_phone_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = Phone(type="PHONE", phone={"number": "+4673522488"})

    assert model.type == "PHONE"
    assert model.phone.number == "+4673522488"


def test_phone_expects_dump_by_alias():
    """Test that the model dumps to the wire representation."""
    model = Phone(type="PHONE", phone={"number": "+4673522488"})

    assert model.model_dump(by_alias=True) == {
        "type": "PHONE",
        "phone": {"number": "+4673522488"},
    }
