from hsrws.data_transformer import transform_char_name


# Test case for basic transformation
def test_transform_basic():
    assert transform_char_name("Harry Potter") == "harry-potter"


# Test case with trailing spaces
def test_transform_with_spaces():
    assert transform_char_name("   Hermione Granger   ") == "-hermione-granger"


# Test case with special characters
def test_transform_with_special_chars():
    assert transform_char_name("Dr. John • Doe") == "dr-john-doe"


# Test case with "(Coming Soon)" suffix
def test_transform_coming_soon():
    assert transform_char_name("Spider-Man (Coming Soon)") == "spider-man"


# Test case with multiple hyphens
def test_transform_multiple_hyphens():
    assert transform_char_name("Iron Man ••• The Avenger") == "iron-man-the-avenger"


# Test case with trailing hyphens
def test_transform_trailing_hyphen():
    assert transform_char_name("Thor -") == "thor"
