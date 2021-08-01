from sqlalchemy import Column, Integer, String, Boolean, DateTime

from ProjectName.app.managing.database import DB


class TimeStamp(DB.Base):
    __tablename__ = 'time_stamp'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    public = Column(Boolean, default=True)
    time = Column(DateTime)
    importance = Column(String, default="low")
