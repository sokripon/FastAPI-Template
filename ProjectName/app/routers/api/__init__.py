from fastapi import APIRouter

from ProjectName.app.routers.api.v1 import router_v1

router_api = APIRouter(prefix="/api", include_in_schema=True)

router_api.include_router(router_v1)



