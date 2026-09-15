from backend.generate import strip_dashes


def test_strip_dashes_replaces_em_dash_with_comma():
    assert strip_dashes("Studio A — great room") == "Studio A, great room"


def test_strip_dashes_replaces_en_dash_with_comma():
    assert strip_dashes("Open 9am – 5pm") == "Open 9am, 5pm"


def test_strip_dashes_leaves_plain_hyphens_alone():
    text = "Our plug-and-play room, designed by Walters-Storyk"
    assert strip_dashes(text) == text


def test_strip_dashes_tidies_comma_period_artifact():
    assert strip_dashes("Great gear — .") == "Great gear."
