import pytest

from main import main


def test_scraper():
    char_data_df = main()

    assert char_data_df.shape[1] == 9
    assert not char_data_df.empty


if __name__ == "__main__":
    pytest.main()
