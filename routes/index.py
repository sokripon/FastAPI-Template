from fastapi import APIRouter
from starlette.requests import Request
from utils.settings import templates
from fastapi.responses import PlainTextResponse
router_root = APIRouter()


@router_root.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "example": "Example"})


@router_root.get("/health")
def health(request: Request):
    return PlainTextResponse("OK")
