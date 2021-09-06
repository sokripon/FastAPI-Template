from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from ProjectName.app.crud.v1.time_stamps import count_all_entries
from ProjectName.app.managing.configs import settings
from ProjectName.app.managing.database import DB
from ProjectName.app.routers.pages import templates

homepage_root = APIRouter()


@homepage_root.get("/")
async def hello_world(request: Request, db: Session = Depends(DB.get_db)):
    we = f"{settings.general.hostname}:{settings.general.port}"
    try:
        if (headers := dict(request._headers)) and headers.get("host") and headers != settings.general.hostname:
            we = headers
    except Exception as e:
        print("Something went horrible wrong with the headers", e)
    return templates.TemplateResponse("index.html",
                                      {"request": request, "time": datetime.now(), "amount": count_all_entries(db),
                                       "websocket": we})
