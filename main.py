from fastapi import FastAPI
from utils.logging import slogger
from middlewares.logging import LoggingMiddleWare
from routes.index import router_root
from models import *  # noqa # used to init the database strcuture

app = FastAPI(title="Template")
app.add_middleware(LoggingMiddleWare)
app.include_router(router=router_root)

slogger.init_logging()
DB.create_myself()

