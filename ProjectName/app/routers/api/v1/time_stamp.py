from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

import ProjectName.app.crud.v1.time_stamps as crud
from ProjectName.app.managing.database import DB
from ProjectName.app.response.schema import ResponseSuccess, ResponseError
from ProjectName.app.response.utils import set_response_success, set_response_error
from ProjectName.app.schemas.time_stamp import TimeStamp, TimeStampCreate, TimeStampDB

router_time = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem, "Other cool tag"])


@router_time.get("/", status_code=status.HTTP_200_OK, response_model=ResponseSuccess[datetime])
async def root(response: Response):
    return set_response_success(response, crud.get_time())


@router_time.post("/add", response_model=ResponseSuccess[TimeStamp], status_code=status.HTTP_201_CREATED)
async def add_new_timestamp(time_stamp: TimeStampCreate, db: Session = Depends(DB.get_db)):
    return crud.create_time_stamp(db, time_stamp)


@router_time.get("/list", status_code=status.HTTP_200_OK, response_model=ResponseSuccess[List[TimeStampDB]])
async def list_times(response: Response, db: Session = Depends(DB.get_db)):
    data = crud.get_all_time_stamp(db)
    return set_response_success(response, data)


@router_time.get("/get/{id}", status_code=404,
                 responses={404: {"model": ResponseError}, 202: {"model": ResponseSuccess[TimeStampDB]}})
async def get_by_id(response: Response, post_id: int = None, db: Session = Depends(DB.get_db)):
    data = crud.get_time_stamp_from_id(db, post_id)
    if data:
        return set_response_success(response, data)
    else:
        return set_response_error(response)
