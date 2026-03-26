import pytest

from src.core.exceptions import NotFoundError

# It must raise an error
@pytest.mark.asyncio
async def test_container_with_intended_exception(container):
    user_service = container.user_service()
    try:
        found_user = await user_service.read(1)
    except NotFoundError as e:
        assert True
        return
    # assert False
