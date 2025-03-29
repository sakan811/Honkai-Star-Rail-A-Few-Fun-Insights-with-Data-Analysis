import pytest
from hsrws.utils.payload import get_first_value


@pytest.fixture
def test_data():
    return {
        "key1": {"values": [10, 20, 30]},
        "key2": {"values": []},
        "key3": {"values": [40]},
    }


def test_get_first_value_non_empty(test_data):
    assert get_first_value(test_data, "key1", "key2") == 10


def test_get_first_value_skip_empty(test_data):
    assert get_first_value(test_data, "key2", "key3") == 40


def test_get_first_value_nonexistent_key(test_data):
    assert (
        get_first_value(test_data, "nonexistent_key", default="Not found")
        == "Not found"
    )


def test_get_first_value_all_empty(test_data):
    assert get_first_value(test_data, "key2", default="Empty") == "Empty"


def test_get_first_value_no_keys(test_data):
    assert get_first_value(test_data, default="No keys") == "No keys"
