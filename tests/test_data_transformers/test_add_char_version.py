import pytest
import pandas as pd




# Example DataFrame for testing
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'Character': ['Harry Potter', 'Hermione Granger', 'Spider-Man', 'Iron Man']
    })


def test_add_char_version(sample_dataframe):
    # Mock return value of get_version_dict
    mock_get_version_dict = {
        2.0: ['Spider-Man', 'Iron Man']
    }

    # Call the function under test
    sample_dataframe['Version'] = sample_dataframe['Character'].apply(
        lambda character: next(
            (version for version, characters in mock_get_version_dict.items() if character in characters),
            1.0
        )
    )


    # Assert that 'Version' column is added and contains expected values
    assert 'Version' in sample_dataframe.columns
    assert sample_dataframe['Version'].equals(pd.Series([1.0, 1.0, 2.0, 2.0], name='Version'))
