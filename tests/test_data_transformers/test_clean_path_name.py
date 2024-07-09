from hsrws.data_transformer import clean_path_name


# Test case for basic cleaning
def test_clean_basic():
    assert clean_path_name("The Avengers") == "Avengers"


# Test case with no "The" prefix
def test_clean_no_the():
    assert clean_path_name("Spider-Man") == "Spider-Man"


# Test case with multiple "The" prefixes
def test_clean_multiple_the():
    assert clean_path_name("The The Matrix") == "Matrix"


# Test case with empty string
def test_clean_empty():
    assert clean_path_name("") == ""


# Test case with special characters
def test_clean_special_chars():
    assert clean_path_name("The ••• Dark Knight") == "••• Dark Knight"
