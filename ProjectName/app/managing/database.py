from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeMeta

from ProjectName.app.managing.configs import settings


class Database:
    # Todo: Make it compatible with multiple databases at once
    # https://github.com/tiangolo/fastapi/issues/2592#issuecomment-773208039
    # https://fastapi.tiangolo.com/advanced/async-sql-databases/ for higher performance
    # https://github.com/tiangolo/fastapi/issues/1825
    # Tortoise ORM maybe? https://tortoise-orm.readthedocs.io/en/latest/examples/fastapi.html
    # ormar maybe? https://github.com/collerek/ormar
    # pony maybe? https://docs.ponyorm.org/integration_with_fastapi.html
    # https://github.com/tortoise/orm-benchmarks
    engine: Engine

    SessionLocal: sessionmaker
    AsyncSession: sessionmaker
    Base: DeclarativeMeta

    def __init__(self):
        self.engine = self._get_database_engine()
        self.async_engine = self._get_database_engine(True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.AsyncSession = sessionmaker(autocommit=False, expire_on_commit=False, autoflush=False,
                                         bind=self.async_engine, class_=AsyncSession)
        self.Base = declarative_base()

    def _get_database_engine(self, asy: bool = False) -> Engine:
        db_in_use = settings.database.dbms

        if db_in_use == "sqlite":
            if asy:
                return self.__get_sqlite_async_engine()
            else:
                return self.__get_sqlite_engine()
        elif db_in_use == "mysql":
            if asy:
                raise NotImplementedError("fuck off")
            return self.__get_mysql_engine()
        else:
            raise NotImplementedError("dbms is not implemented yet")

    @staticmethod
    def __get_mysql_engine() -> Engine:
        return create_async_engine(
            f"mysql+mysqlconnector://{settings.database.username}:{settings.database.password}@{settings.database.host}:{settings.database.port}/{settings.database.name}",
            connect_args={"check_same_thread": False})

    @staticmethod
    def __get_sqlite_engine() -> Engine:
        return create_engine(f"sqlite:///{Path(__file__).parent.parent.parent}/{settings.database.name}",
                             connect_args={"check_same_thread": False})

    @staticmethod
    def __get_sqlite_async_engine() -> Engine:
        return create_async_engine(
            f"sqlite+aiosqlite:///{Path(__file__).parent.parent.parent}/{settings.database.name}",
            connect_args={"check_same_thread": False})

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def get_db_async(self):
        db = self.AsyncSession()
        try:
            yield db
        finally:
            await db.close()


DB = Database()
