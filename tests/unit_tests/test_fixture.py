import pytest

@pytest.mark.asyncio
async def test_test_name_fixture(test_name):
    assert test_name == "test_test_name_fixture"
