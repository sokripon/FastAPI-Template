from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeMeta

from utils.settings import setting


class Database:
    engine: Engine

    SessionLocal: sessionmaker
    Base: DeclarativeMeta

    def __init__(self, db_url: str, sync=True):
        connect_args = None
        if db_url.startswith("sqlite"):
            connect_args = {'check_same_thread': False}
        if sync:
            self.engine = create_engine(db_url, echo=False, connect_args=connect_args)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=self.engine)
        else:
            self.engine = create_async_engine(db_url, echo=False, connect_args=connect_args)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=self.engine, expire_on_commit=False, class_=AsyncSession)

        self.Base = declarative_base()

    async def create_myself_async(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)
        # In use:
        # async with DB.SessionLocal() as session:

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_myself(self):
        self.Base.metadata.create_all(bind=self.engine)

    class DBContextManager:
        def __init__(self, db):
            self.db = db

        def __enter__(self):
            return self.db

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.db.close()


DB = Database(setting.database_url)
