from typing import AsyncGenerator


from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


async_engine = create_async_engine(settings.database_url)

async_session_factory = async_sessionmaker(async_engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as async_session:
        try:
            yield async_session
        except Exception as e:
            await async_session.rollback()
            raise e
        finally:
            await async_session.close()


class Base(DeclarativeBase):

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col=}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {','.join(cols)}>"
