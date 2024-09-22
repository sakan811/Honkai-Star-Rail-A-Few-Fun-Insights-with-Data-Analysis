import pytest

from hsrws.hsr_scraper import get_payload


@pytest.mark.asyncio
async def test_get_payload():
    page_num = 1
    expected_payload = {
        "filters": [],
        "menu_id": "104",
        "page_num": page_num,
        "page_size": 30,
        "use_es": True
    }

    payload = await get_payload(page_num)
    assert payload == expected_payload

    page_num = 2
    expected_payload["page_num"] = page_num

    payload = await get_payload(page_num)
    assert payload == expected_payload

if __name__ == '__main__':
    pytest.main()