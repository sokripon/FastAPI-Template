from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from ProjectName.app.managing.configs import settings
from ProjectName.app.managing.database import DB
from ProjectName.app.middlewares.example import CustomMiddleWare
from ProjectName.app.routers import page_routers, api_routers

DB.Base.metadata.create_all(bind=DB.engine)

app = FastAPI(title=settings.general.project_name, description="Template for an not so good api",
              contact={"name": "sokripon", "email": "sokripon@gmail.com"})

app.mount("/static", StaticFiles(directory=Path(__file__).parent.__str__() + "/static"), name="static")


@app.on_event("shutdown")
def shutdown():
    pass


app.add_middleware(CustomMiddleWare)
app.include_router(router=page_routers)
app.include_router(router=api_routers)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.general.hostname, port=settings.general.port, reload=settings.general.reload)
