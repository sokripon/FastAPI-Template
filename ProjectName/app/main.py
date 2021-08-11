import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from pathlib import Path
import logging
import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.staticfiles import StaticFiles

from ProjectName.app.managing.configs import settings
from ProjectName.app.managing.database import DB
from ProjectName.app.middlewares.example import CustomMiddleWare
from ProjectName.app.routers import page_routers, api_routers
from ProjectName.app.ws import ConnectionManager
from ProjectName.app.ws import ws_routers

DB.create_myself()
log = logging.getLogger("uvicorn")
log.info(f"Uvicorn running on http://{settings.general.hostname}:{settings.general.port}")

app = FastAPI(title=settings.general.project_name, description="Template for an not so good api",
              contact={"name": "sokripon", "email": "sokripon@gmail.com"})
app.mount("/static", StaticFiles(directory=Path(__file__).parent.__str__() + "/static"), name="static")


@app.on_event("shutdown")
def shutdown():
    log.info("Application shutting down.")


@app.on_event("startup")
async def startup_fun():
    log.info("Application startup complete.")


@app.on_event("startup")
@repeat_every(seconds=5)
async def ehe_te_nandayo_task() -> None:
    await ConnectionManager.manager.broadcast("ehe")


app.add_middleware(CustomMiddleWare)
app.include_router(router=page_routers)
app.include_router(router=api_routers)
app.include_router(router=ws_routers)
log.info(f"Started server process [{os.getpid()}]")
if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.general.hostname, port=settings.general.port, reload=settings.general.reload,
                log_level=logging.WARNING, workers=1, use_colors=True, reload_dirs=f"{Path(__file__).parent.__str__()}")
