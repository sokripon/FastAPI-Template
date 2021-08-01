import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.staticfiles import StaticFiles

from ProjectName.app.managing.configs import settings
from ProjectName.app.managing.database import DB
from ProjectName.app.middlewares.example import CustomMiddleWare
from ProjectName.app.routers import page_routers, api_routers

log = logging.getLogger("uvicorn")
log.info(f"Uvicorn running on http://{settings.general.hostname}:{settings.general.port}")
DB.Base.metadata.create_all(bind=DB.engine)

app = FastAPI(title=settings.general.project_name, description="Template for an not so good api",
              contact={"name": "sokripon", "email": "sokripon@gmail.com"})
app.mount("/static", StaticFiles(directory=Path(__file__).parent.__str__() + "/static"), name="static")


@app.on_event("shutdown")
def shutdown():
    log.info("Application shutting down.")


@app.on_event("startup")
def kek():
    log.info("Application startup complete.")


from ProjectName.app.ws import ConnectionManager


@app.on_event("startup")
@repeat_every(seconds=5)
async def remove_expired_tokens_task() -> None:
    await ConnectionManager.manager.broadcast("ehe")


if __name__ == "main":
    # uvicorn command will not work with this
    from ProjectName.app.ws import *  # Idk why but yes

    app.add_middleware(CustomMiddleWare)
    app.include_router(router=page_routers)
    app.include_router(router=api_routers)
    log.info(f"Started server process [{os.getpid()}]")
if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.general.hostname, port=settings.general.port, reload=settings.general.reload,
                log_level=logging.WARNING, workers=2, use_colors=True)
