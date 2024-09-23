from fastapi import APIRouter

from src.routers.trade_mark_router import trade_mark_router


router = APIRouter(prefix='/api/v1')

router.include_router(router=trade_mark_router)

__all__ = ('router',)
