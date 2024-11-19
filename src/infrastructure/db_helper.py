from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings


class DatabaseHelper:
    def __init__(self) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=str(settings.db_config.SQLALCHEMY_DATABASE_URI),
            echo=False,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


#     async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
#         async with self.session_factory() as session:
#             try:
#                 yield session
#             finally:
#                 await session.close()


# db_helper = DatabaseHelper(
#     url=str(db_config.SQLALCHEMY_DATABASE_URI),
#     echo=False,
# )

# DbSession = Annotated[AsyncSession, Depends(db_helper.session_dependency)]
