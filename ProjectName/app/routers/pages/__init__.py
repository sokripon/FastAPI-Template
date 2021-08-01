from pathlib import Path

from fastapi import APIRouter
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent.__str__() + "/templates")

from ProjectName.app.routers.pages.index import homepage_root

router_pages = APIRouter(tags=["pages"], include_in_schema=False)

router_pages.include_router(homepage_root)
