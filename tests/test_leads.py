from backend.leads import extract_lead


def test_extract_lead_email_only():
    lead = extract_lead("Hi, I'd like a quote. My email is jane@example.com")
    assert lead == {
        "type": "general_inquiry",
        "email": "jane@example.com",
        "phone": None,
        "message": "Hi, I'd like a quote. My email is jane@example.com",
    }


def test_extract_lead_phone_only():
    lead = extract_lead("Call me at +49 176 12345678 about Studio A")
    assert lead["email"] is None
    assert lead["phone"] == "+49 176 12345678"


def test_extract_lead_both_email_and_phone():
    lead = extract_lead("Reach me at jane@example.com or +49 176 12345678")
    assert lead["email"] == "jane@example.com"
    assert lead["phone"] == "+49 176 12345678"


def test_extract_lead_neither_returns_none():
    assert extract_lead("What time do you open on Saturdays?") is None


def test_extract_lead_phone_too_short_is_ignored():
    # 8 digits, below the 9-digit floor: not treated as a real phone number.
    assert extract_lead("My number is 12345678, call me") is None


def test_extract_lead_phone_minimum_valid_length():
    # 9 digits: the floor of the accepted range.
    lead = extract_lead("My number is 123456789, call me")
    assert lead["phone"] == "123456789"


def test_extract_lead_phone_maximum_valid_length():
    # 15 digits: the ceiling of the accepted (E.164-ish) range.
    lead = extract_lead("My number is 123456789012345, call me")
    assert lead["phone"] == "123456789012345"


def test_extract_lead_phone_too_long_is_ignored():
    # 16 digits, above the 15-digit ceiling: not treated as a real phone number.
    assert extract_lead("My number is 1234567890123456, call me") is None
