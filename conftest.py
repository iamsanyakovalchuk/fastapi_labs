import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# Імпортуємо наш додаток, базу та моделі
from app.main import app
from app.core.db import get_session
from app.models.models import Base

# 1. URL до нашої ТЕСТОВОЇ бази даних (зверни увагу на fastapi_test_db)
# Заміни 'postgres' та 'password' на ті, що у тебе в docker-compose, якщо вони відрізняються.
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@db:5432/fastapi_test_db"

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def prepare_database():
    """Перед кожним тестом створюємо таблиці, а після - видаляємо"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    """Створює сесію для тестової БД"""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session):
    """Підміняє get_session на тестову і видає клієнта для запитів"""

    async def override_get_session():
        yield db_session

    # ОСЬ ВОНА - ПІДМІНА ЗАЛЕЖНОСТЕЙ!
    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()