from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from ProjectName.app.models import TimeStamp as TimeStampM
from ProjectName.app.schemas import TimeStampCreate, TimeStampDBBase, TimeStampDB


def get_time() -> str:
    return datetime.now().__str__()


def create_time_stamp(db: Session, time_st: TimeStampCreate) -> TimeStampDBBase:
    db_time = TimeStampM(name=time_st.name, public=time_st.public, time=time_st.time,
                         importance=time_st.importance)
    db.add(db_time)
    db.commit()
    db.refresh(db_time)
    return db_time


def get_time_stamp_from_id(db: Session, id: int) -> Optional[TimeStampDB]:
    data = db.query(TimeStampM).filter(TimeStampM.id == id).first()
    if data:
        return TimeStampDB(**data.__dict__)
    else:
        return None


def get_all_time_stamp(db: Session) -> List[Optional[TimeStampDB]]:
    return db.query(TimeStampM).all()


def count_all_entries(db: Session) -> int:
    return db.query(TimeStampM).count()
