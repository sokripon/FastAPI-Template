from fastapi import APIRouter
from starlette.requests import Request
from utils.settings import templates

router_root = APIRouter()


@router_root.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "example": "Example"})
