from fastapi import APIRouter

from ProjectName.app.routers.api import router_api
from ProjectName.app.routers.pages import router_pages

api_routers = APIRouter()
api_routers.include_router(router_api)

page_routers = APIRouter()
page_routers.include_router(router_pages)
