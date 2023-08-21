from fastapi import APIRouter

from app.api.api_v1 import api_common, router_v1

router = APIRouter()

router.include_router(api_common.router, tags=["Common"])
router.include_router(router_v1, prefix="/v1")
