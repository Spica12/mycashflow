import contextlib

from sqlalchemy.ext.asyncio import (AsyncEngine,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.config.settings import settings
from src.utils.logging import logger


class DataBaseSessionManager:
    def __init__(self, url: str):
        self.engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self.engine, expire_on_commit=False,
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            logger.error("Session is not initialized")
            raise Exception("Session is not initialized")
        session = self._session_maker()
        logger.debug(f"Session ID: {id(session)}")
        try:
            yield session
        except Exception as e:
            logger.error(e)
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.info("Session closed")


sessionmanager = DataBaseSessionManager(settings.db.DB_URL)


# @contextlib.asynccontextmanager
async def get_db():
    async with sessionmanager.session() as session:
        logger.debug("Start. Session ID: id = %s", id(session))
        yield session
        logger.debug("Finish. Session ID: id = %s", id(session))

async def check_db_connection() -> bool:
    try:
        async with sessionmanager.session() as session:
            # Виконуємо простий запит для перевірки з'єднання
            result = await session.execute(select(1))
            if result.scalar() == 1:
                logger.info("Database connection is successful.")
                return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        return False
