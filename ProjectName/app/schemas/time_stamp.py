import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# Of course you would NOT use strings for that, this is just for example usage and I'm not creative
class Importance(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TimeStampBase(BaseModel):
    name: str
    public: Optional[bool] = True
    time: datetime.datetime
    importance: Optional[Importance] = Importance.low


class TimeStampCreate(TimeStampBase):
    time: datetime.datetime = Field(datetime.datetime.now(), description="Defaults to current time")


class TimeStampUpdate(TimeStampBase):
    name: str
    time: datetime.datetime
    importance: Optional[Importance] = Importance.low


class TimeStampDBBase(TimeStampBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class TimeStamp(TimeStampDBBase):
    pass


class TimeStampDB(TimeStampDBBase):
    pass
