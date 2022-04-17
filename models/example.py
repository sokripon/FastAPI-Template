from sqlalchemy import Column, Integer, String, Boolean, DateTime

from utils.database import DB


class Example(DB.Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
