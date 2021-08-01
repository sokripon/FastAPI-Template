from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

from ProjectName.app.managing.configs import settings


class Database:
    # Todo: Make it compatible with multiple databases at once
    # https://github.com/tiangolo/fastapi/issues/2592#issuecomment-773208039
    # https://fastapi.tiangolo.com/advanced/async-sql-databases/ for higher performance
    # https://github.com/tiangolo/fastapi/issues/1825
    # Tortoise ORM maybe? https://tortoise-orm.readthedocs.io/en/latest/examples/fastapi.html
    # ormar maybe? https://github.com/collerek/ormar
    engine: Engine

    SessionLocal: sessionmaker
    Base: DeclarativeMeta

    def __init__(self):
        self.engine = self._get_database_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=self.engine)
        self.Base = declarative_base()
        self.debug = id(self)

    def _get_database_engine(self) -> Engine:
        db_in_use = settings.database.dbms
        if db_in_use == "sqlite":
            return self.__get_sqlite_engine()
        elif db_in_use == "mysql":
            return self.__get_mysql_engine()
        else:
            raise NotImplementedError("dbms is not implemented yet")

    @staticmethod
    def __get_mysql_engine() -> Engine:
        return create_engine(
            f"mysql+mysqlconnector://{settings.database.username}:{settings.database.password}@{settings.database.host}:{settings.database.port}/{settings.database.name}")

    @staticmethod
    def __get_sqlite_engine() -> Engine:
        return create_engine(f"sqlite:///{Path(__file__).parent.parent.parent}/{settings.database.name}",
                             connect_args={"check_same_thread": False})

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


DB = Database()
