from fastapi import APIRouter

from app.api.api_v1 import (api_healthcheck)

router_v1 = APIRouter()

router_v1.include_router(api_healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")
