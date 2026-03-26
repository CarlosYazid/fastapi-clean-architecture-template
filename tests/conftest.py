import json
import os
from pathlib import Path

import aiofiles
import pytest_asyncio
from loguru import logger
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.settings import get_settings
from src.core.container import Container
from src.main import AppCreator
from src.model.user import User

BASE_DIR = Path(__file__).resolve().parent
os.environ["ENV"] = "test"

async def insert_default_data(conn):
    
    user_default_data = []
    
    async with aiofiles.open(BASE_DIR / "test_data" / "users.json", "r") as user_default_file:
        user_default_data = json.loads(await user_default_file.read())
    
    await conn.execute(User.__table__.insert(), user_default_data)

async def reset_db():
    
    engine = create_async_engine(get_settings().DATABASE_URI)
    
    logger.info(engine)

    async with engine.begin() as conn:
        if "test" in get_settings().ENV:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
            await insert_default_data(conn)
        else:
            raise Exception("Not in test environment")

    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def setup_db():
    await reset_db()
    yield

@pytest_asyncio.fixture
async def client(setup_db):

    app_creator = AppCreator()
    app = app_creator.app
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test') as client:
        yield client

@pytest_asyncio.fixture
async def container():
    return Container()

@pytest_asyncio.fixture
async def test_name(request):
    return request.node.name