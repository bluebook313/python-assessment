from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from schemas.config import DATABASE_URL
from schemas.config import log
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    try:
        async with AsyncSessionLocal() as db:
            yield db
    except Exception as e:
        log.error(f"Error in connection to db")
        raise 