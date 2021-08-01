from fastapi import APIRouter, Request
from starlette.responses import PlainTextResponse, RedirectResponse

from .time_stamp import router_time

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(router_time)


@router_v1.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")
