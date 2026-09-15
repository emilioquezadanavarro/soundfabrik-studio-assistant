from backend.guard import BOOKING_KEYWORDS, STUDIO_TERMS, looks_like_booking


def test_studio_terms_hits_on_room_and_gear_mentions():
    assert STUDIO_TERMS.search("Do you have a Neve console in Studio A?")


def test_studio_terms_hits_on_booking_language():
    assert STUDIO_TERMS.search("What's your availability next week?")


def test_studio_terms_misses_unrelated_message():
    assert not STUDIO_TERMS.search("What's the weather like today?")


def test_looks_like_booking_hits_on_cost_question():
    assert looks_like_booking("How much does a session cost?")


def test_looks_like_booking_hits_on_reservation_language():
    assert looks_like_booking("I'd like to reserve a slot next month")


def test_looks_like_booking_misses_gear_question():
    assert not looks_like_booking("Tell me about the grand piano")


def test_booking_keywords_regex_directly():
    assert BOOKING_KEYWORDS.search("Can I get a quote?")
    assert not BOOKING_KEYWORDS.search("Who plays the Steinway?")
