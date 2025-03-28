import pytest

from hsrws.data_transformer import transform_char_name


# Test case for basic transformation
@pytest.mark.parametrize(
    "input_name, expected_output",
    [
        ("Harry Potter", "harry-potter"),  # Basic test case
        ("   Hermione Granger   ", "-hermione-granger"),  # Trailing spaces
        ("Dr. John • Doe", "dr-john-doe"),  # Special characters
        ("Spider-Man (Coming Soon)", "spider-man"),  # "(Coming Soon)" suffix
        ("Iron Man ••• The Avenger", "iron-man-the-avenger"),  # Multiple hyphens
        ("Thor -", "thor"),  # Trailing hyphens
        ("March 7th\u00a0: The Hunt", "march-7th-the-hunt"),
    ],
)
def test_transform(input_name, expected_output):
    assert transform_char_name(input_name) == expected_output
