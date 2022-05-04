from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from utils.logging import slogger
from middlewares.logging import LoggingMiddleWare
from routes.index import router_root
from models import *  # noqa # used to init the database strcuture
from utils.settings import setting

app = FastAPI(title="Template", description="Template API", version="0.1.0", docs_url=setting.docs_url, redoc_url=setting.redoc_url, openapi_url=setting.openapi_url)
app.add_middleware(LoggingMiddleWare)
app.include_router(router=router_root)
app.mount("/static", StaticFiles(directory="static"), name="static")

slogger.init_logging()
DB.create_myself()

